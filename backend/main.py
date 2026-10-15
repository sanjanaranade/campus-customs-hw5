"""FastAPI backend for the Campus Customs dashboard."""

from __future__ import annotations

import json
import shutil
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from backend.config import AUDIT_PATH, DATABASE_PATH
from backend.models import TeamRunLimits
from backend.team_loop import run_team


ORIGINAL_DATABASE = PROJECT_DIR / "data" / "campus_customs.db"

app = FastAPI(title="Campus Customs Operations API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RunRequest(BaseModel):
    max_steps: int = Field(default=24, ge=1, le=24)
    max_delegations: int = Field(default=12, ge=0, le=12)


class ApprovalRequest(BaseModel):
    kind: str = Field(pattern="^(invoice|rent)$")
    ref_id: int = Field(gt=0)
    amount: float = Field(gt=0)
    account: str = Field(min_length=1)
    approved_by: str = Field(min_length=1, max_length=200)


def connect(read_only: bool = False) -> sqlite3.Connection:
    if not DATABASE_PATH.is_file():
        raise HTTPException(status_code=500, detail=f"Working database not found: {DATABASE_PATH}")
    if read_only:
        db = sqlite3.connect(f"file:{DATABASE_PATH}?mode=ro", uri=True)
    else:
        db = sqlite3.connect(DATABASE_PATH)
    db.row_factory = sqlite3.Row
    return db


def rows(query: str, params: tuple = ()) -> list[dict]:
    with connect(read_only=True) as db:
        return [dict(row) for row in db.execute(query, params).fetchall()]


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "database": str(DATABASE_PATH), "model": "gpt-6-luna"}


@app.get("/tickets")
def get_tickets(status: str | None = Query(default=None, pattern="^(open|closed)$")) -> list[dict]:
    """Return tickets, optionally filtered to the dashboard's open/closed state."""

    if status:
        return rows("SELECT * FROM tickets WHERE status = ? ORDER BY id", (status,))
    return rows("SELECT * FROM tickets ORDER BY id")


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int) -> dict:
    result = rows("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    if not result:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return result[0]


@app.post("/tickets/{ticket_id}/run")
async def run_agent_team(ticket_id: int, request: RunRequest | None = None) -> dict:
    """Run the bounded team loop for exactly one open ticket."""

    ticket = get_ticket(ticket_id)
    if ticket["status"] != "open":
        raise HTTPException(status_code=409, detail="Only open tickets can be run")
    limits = request or RunRequest()
    result = await run_team(
        [ticket],
        TeamRunLimits(
            max_steps=limits.max_steps,
            max_delegations=limits.max_delegations,
            max_model_calls=0,
        ),
    )
    return result.model_dump(mode="json")


@app.get("/events")
def get_recent_events(limit: int = Query(default=50, ge=1, le=200)) -> list[dict]:
    """Return the newest audit events for board refreshes."""

    if not AUDIT_PATH.exists():
        return []
    try:
        events = json.loads(AUDIT_PATH.read_text())
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail="Audit trail is invalid JSON") from exc
    return events[-limit:]


@app.get("/cash/checking")
def get_checking_balance() -> dict:
    result = rows("SELECT * FROM cash_accounts WHERE name = 'checking'")
    if not result:
        raise HTTPException(status_code=404, detail="Checking account not found")
    return result[0]


@app.post("/payments/approve")
def approve_payment(request: ApprovalRequest) -> dict:
    """Execute a human-approved invoice or rent payment atomically."""

    with connect() as db:
        cash = db.execute(
            "SELECT balance FROM cash_accounts WHERE name = ?", (request.account,)
        ).fetchone()
        if cash is None:
            raise HTTPException(status_code=404, detail="Cash account not found")
        if cash["balance"] < request.amount:
            raise HTTPException(status_code=409, detail="Payment refused: insufficient cash")
        if request.kind == "invoice":
            source = db.execute(
                "SELECT id, status FROM invoices WHERE id = ?", (request.ref_id,)
            ).fetchone()
            if source is None:
                raise HTTPException(status_code=404, detail="Invoice not found")
            if source["status"] == "paid":
                raise HTTPException(status_code=409, detail="Invoice is already paid")
        else:
            source = db.execute(
                "SELECT id FROM leases WHERE id = ?", (request.ref_id,)
            ).fetchone()
            if source is None:
                raise HTTPException(status_code=404, detail="Lease not found")

        paid_at = db.execute("SELECT date_today FROM desk LIMIT 1").fetchone()[0]
        db.execute(
            "UPDATE cash_accounts SET balance = balance - ?, date = ? WHERE name = ?",
            (request.amount, paid_at, request.account),
        )
        cursor = db.execute(
            """
            INSERT INTO payments(kind, ref_id, amount, account, paid_at, approved_by)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (request.kind, request.ref_id, request.amount, request.account, paid_at, request.approved_by),
        )
        if request.kind == "invoice":
            db.execute("UPDATE invoices SET status = 'paid' WHERE id = ?", (request.ref_id,))
        db.commit()
        balance = db.execute(
            "SELECT balance FROM cash_accounts WHERE name = ?", (request.account,)
        ).fetchone()[0]
    return {
        "payment_id": cursor.lastrowid,
        "kind": request.kind,
        "ref_id": request.ref_id,
        "amount": request.amount,
        "account": request.account,
        "balance_after": balance,
        "approved_by": request.approved_by,
        "paid_at": paid_at,
    }


@app.post("/reset")
def reset_database() -> dict:
    """Restore the working copy from the untouched original database."""

    if not ORIGINAL_DATABASE.is_file():
        raise HTTPException(status_code=500, detail="Original database not found")
    shutil.copy2(ORIGINAL_DATABASE, DATABASE_PATH)
    return {"status": "reset", "database": str(DATABASE_PATH), "source_untouched": True}
