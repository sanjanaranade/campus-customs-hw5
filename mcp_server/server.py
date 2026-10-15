"""Read-only MCP tools for the Campus Customs working database.

The database is opened only when a tool is called. Importing this module does
not connect to the database or start the MCP server.
"""

from __future__ import annotations

import os
import sqlite3
from pathlib import Path
from typing import Any

from fastmcp import FastMCP


PROJECT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_DATABASE = PROJECT_DIR / "data" / "campus_customs_new.db"

mcp = FastMCP("Campus Customs Operations")


def _database_path() -> Path:
    """Return the configured working database path without opening it."""

    configured = os.environ.get("CAMPUS_CUSTOMS_DB")
    return Path(configured).expanduser() if configured else DEFAULT_DATABASE


def _connect() -> sqlite3.Connection:
    """Open the working database for one read-only tool invocation."""

    database = _database_path()
    if not database.is_file():
        raise FileNotFoundError(f"Working database not found: {database}")
    connection = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection


def _connect_rw() -> sqlite3.Connection:
    """Open the working database for explicitly permitted board writes."""

    database = _database_path()
    if not database.is_file():
        raise FileNotFoundError(f"Working database not found: {database}")
    connection = sqlite3.connect(database)
    connection.row_factory = sqlite3.Row
    return connection


def _row_dict(row: sqlite3.Row | None) -> dict[str, Any] | None:
    return dict(row) if row is not None else None


@mcp.tool()
def list_open_tickets() -> list[dict[str, Any]]:
    """List every ticket whose status is exactly ``open``."""

    with _connect() as connection:
        rows = connection.execute(
            """
            SELECT id, type, requester, subject, sku, size, qty,
                   lease_id, invoice_id, status, notes, created_at
            FROM tickets
            WHERE status = 'open'
            ORDER BY id
            """
        ).fetchall()
    return [dict(row) for row in rows]


@mcp.tool()
def get_ticket_full_context(ticket_id: int) -> dict[str, Any]:
    """Return a ticket and all directly linked lease, invoice, vendor,
    inventory, and pricing records available in the database.
    """

    with _connect() as connection:
        ticket = connection.execute(
            "SELECT * FROM tickets WHERE id = ?", (ticket_id,)
        ).fetchone()
        if ticket is None:
            raise ValueError(f"Ticket {ticket_id} was not found")

        ticket_data = dict(ticket)
        inventory = None
        pricing = None
        lease = None
        invoice = None
        vendor = None

        if ticket["sku"] is not None and ticket["size"] is not None:
            inventory = _row_dict(
                connection.execute(
                    "SELECT * FROM inventory WHERE sku = ? AND size = ?",
                    (ticket["sku"], ticket["size"]),
                ).fetchone()
            )
        if ticket["sku"] is not None:
            pricing = _row_dict(
                connection.execute(
                    "SELECT * FROM pricing WHERE sku = ?", (ticket["sku"],)
                ).fetchone()
            )
        if ticket["lease_id"] is not None:
            lease = _row_dict(
                connection.execute(
                    "SELECT * FROM leases WHERE id = ?", (ticket["lease_id"],)
                ).fetchone()
            )
        if ticket["invoice_id"] is not None:
            invoice = _row_dict(
                connection.execute(
                    "SELECT * FROM invoices WHERE id = ?", (ticket["invoice_id"],)
                ).fetchone()
            )
            if invoice is not None:
                vendor = _row_dict(
                    connection.execute(
                        "SELECT * FROM vendors WHERE id = ?",
                        (invoice["vendor_id"],),
                    ).fetchone()
                )

    return {
        "ticket": ticket_data,
        "inventory": inventory,
        "pricing": pricing,
        "lease": lease,
        "invoice": invoice,
        "vendor": vendor,
    }


@mcp.tool()
def get_ticket_restock_and_financial_context(ticket_id: int) -> dict[str, Any]:
    """Calculate stock shortage and margin facts for a ticket, and return
    linked vendor-invoice and cash facts when those records exist.

    This tool reports facts and calculations only. It does not place orders,
    create payments, change balances, or contact anyone.
    """

    context = get_ticket_full_context(ticket_id)
    ticket = context["ticket"]
    inventory = context["inventory"]
    pricing = context["pricing"]
    invoice = context["invoice"]
    vendor = context["vendor"]

    requested_qty = ticket["qty"]
    stock_qty = inventory["qty"] if inventory is not None else None
    shortage_qty = None
    if requested_qty is not None and stock_qty is not None:
        shortage_qty = max(requested_qty - stock_qty, 0)

    unit_margin = None
    if pricing is not None:
        unit_margin = pricing["list_price"] - pricing["unit_cost"]

    with _connect() as connection:
        shop_date = connection.execute(
            "SELECT date_today FROM desk LIMIT 1"
        ).fetchone()
        cash_accounts = [
            dict(row)
            for row in connection.execute(
                "SELECT name, balance, date FROM cash_accounts ORDER BY name"
            ).fetchall()
        ]

        unpaid_vendor_invoice_count = None
        if vendor is not None:
            unpaid_vendor_invoice_count = connection.execute(
                """
                SELECT COUNT(*)
                FROM invoices
                WHERE vendor_id = ? AND status != 'paid'
                """,
                (vendor["id"],),
            ).fetchone()[0]

    return {
        "ticket_id": ticket_id,
        "shop_date": shop_date["date_today"] if shop_date else None,
        "requested_qty": requested_qty,
        "stock_qty": stock_qty,
        "shortage_qty": shortage_qty,
        "unit_margin": unit_margin,
        "linked_invoice": invoice,
        "linked_vendor": vendor,
        "linked_vendor_unpaid_invoice_count": unpaid_vendor_invoice_count,
        "cash_accounts": cash_accounts,
    }


@mcp.tool()
def get_lease_rent_context(ticket_id: int) -> dict[str, Any]:
    """Return the linked lease and authoritative shop date for a ticket."""

    with _connect() as connection:
        ticket = connection.execute(
            "SELECT id, lease_id, status FROM tickets WHERE id = ?", (ticket_id,)
        ).fetchone()
        if ticket is None:
            raise ValueError(f"Ticket {ticket_id} was not found")
        desk = connection.execute("SELECT * FROM desk LIMIT 1").fetchone()
        lease = None
        if ticket["lease_id"] is not None:
            lease = connection.execute(
                "SELECT * FROM leases WHERE id = ?", (ticket["lease_id"],)
            ).fetchone()
    return {
        "ticket": dict(ticket),
        "shop_date": _row_dict(desk),
        "lease": _row_dict(lease),
    }


@mcp.tool()
def list_restock_vendor_options(sku: str, size: str) -> dict[str, Any]:
    """Return the recorded product and vendors whose specialties contain a
    product-name keyword, with any unpaid-invoice block explicitly reported.
    """

    with _connect() as connection:
        product = connection.execute(
            """
            SELECT i.sku, i.name, i.size, i.qty, p.unit_cost, p.list_price
            FROM inventory i LEFT JOIN pricing p ON p.sku = i.sku
            WHERE i.sku = ? AND i.size = ?
            """,
            (sku, size),
        ).fetchone()
        if product is None:
            raise ValueError(f"Inventory record not found for {sku} size {size}")
        name_terms = [term for term in product["name"].lower().split() if len(term) >= 4]
        vendors = []
        for vendor in connection.execute("SELECT * FROM vendors ORDER BY id").fetchall():
            specialty = vendor["specialty"].lower()
            specialty_match = any(term in specialty for term in name_terms)
            unpaid_count = connection.execute(
                "SELECT COUNT(*) FROM invoices WHERE vendor_id = ? AND status != 'paid'",
                (vendor["id"],),
            ).fetchone()[0]
            vendors.append({
                **dict(vendor),
                "specialty_match": specialty_match,
                "unpaid_invoice_count": unpaid_count,
                "shipment_allowed": specialty_match and unpaid_count == 0,
            })
    return {"product": dict(product), "vendors": vendors}


@mcp.tool()
def prepare_payment_request(kind: str, ref_id: int, amount: float, account: str) -> dict[str, Any]:
    """Prepare a human approval request without moving cash or writing tables."""

    if amount <= 0:
        raise ValueError("Payment amount must be positive")
    with _connect() as connection:
        cash = connection.execute(
            "SELECT name, balance FROM cash_accounts WHERE name = ?", (account,)
        ).fetchone()
    if cash is None:
        raise ValueError(f"Cash account not found: {account}")
    return {
        "kind": kind,
        "ref_id": ref_id,
        "amount": amount,
        "account": account,
        "current_balance": cash["balance"],
        "would_leave_balance": cash["balance"] - amount,
        "eligible_for_human_review": cash["balance"] >= amount,
        "requires_human_approval": True,
        "side_effects": "none",
    }


@mcp.tool()
def get_payment_status_context(ticket_id: int) -> dict[str, Any]:
    """Return actual linked invoice/payment records and cash accounts for a ticket."""

    with _connect() as connection:
        ticket = connection.execute(
            "SELECT id, lease_id, invoice_id, status FROM tickets WHERE id = ?",
            (ticket_id,),
        ).fetchone()
        if ticket is None:
            raise ValueError(f"Ticket {ticket_id} was not found")
        invoice = None
        if ticket["invoice_id"] is not None:
            invoice = connection.execute(
                "SELECT * FROM invoices WHERE id = ?", (ticket["invoice_id"],)
            ).fetchone()
        payments = []
        if invoice is not None:
            payments = [dict(row) for row in connection.execute(
                "SELECT * FROM payments WHERE kind = 'invoice' AND ref_id = ? ORDER BY id",
                (invoice["id"],),
            ).fetchall()]
        if ticket["lease_id"] is not None:
            payments.extend(dict(row) for row in connection.execute(
                "SELECT * FROM payments WHERE kind = 'rent' AND ref_id = ? ORDER BY id",
                (ticket["lease_id"],),
            ).fetchall())
        cash_accounts = [dict(row) for row in connection.execute(
            "SELECT * FROM cash_accounts ORDER BY name"
        ).fetchall()]
    return {
        "ticket": dict(ticket),
        "invoice": _row_dict(invoice),
        "payments": payments,
        "cash_accounts": cash_accounts,
    }


@mcp.tool()
def append_ticket_note(ticket_id: int, note: str) -> dict[str, Any]:
    """Append a board note to an existing ticket; never sends it externally."""

    if not note.strip():
        raise ValueError("Note must not be empty")
    with _connect_rw() as connection:
        ticket = connection.execute(
            "SELECT id, notes FROM tickets WHERE id = ?", (ticket_id,)
        ).fetchone()
        if ticket is None:
            raise ValueError(f"Ticket {ticket_id} was not found")
        prior = ticket["notes"] or ""
        combined = f"{prior}\n{note.strip()}" if prior else note.strip()
        connection.execute(
            "UPDATE tickets SET notes = ? WHERE id = ?", (combined, ticket_id)
        )
        connection.commit()
    return {"ticket_id": ticket_id, "notes": combined, "external_contact_sent": False}


if __name__ == "__main__":
    mcp.run()
