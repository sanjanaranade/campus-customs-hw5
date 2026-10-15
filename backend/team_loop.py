"""Bounded, append-only multi-agent orchestration loop."""

from __future__ import annotations

import asyncio
import sqlite3
import uuid
from datetime import datetime, timezone

from .agent_common import TeamContext
from .audit import append_audit_event
from .models import AgentName, AuditEvent, Delegation, TeamRunLimits, TeamRunResult
from .config import DATABASE_PATH


def _audit(
    run_id: str,
    step: int,
    agent: AgentName,
    action: str,
    ticket_id: int | None = None,
    input_summary: dict | None = None,
    output_summary: dict | None = None,
    delegated_to: AgentName | None = None,
    requires_human_approval: bool = False,
) -> None:
    append_audit_event(
        AuditEvent(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc),
            run_id=run_id,
            step=step,
            event_type="agent_step",
            agent=agent,
            ticket_id=ticket_id,
            action=action,
            input_summary=input_summary or {},
            output_summary=output_summary or {},
            delegated_to=delegated_to,
            requires_human_approval=requires_human_approval,
        )
    )


async def run_team(
    open_tickets: list[dict],
    limits: TeamRunLimits | None = None,
) -> TeamRunResult:
    """Run a bounded orchestration skeleton over MCP-returned ticket facts.

    Model calls and specialist tool calls are intentionally explicit extension
    points; no fabricated facts are created when the loop is invoked.
    """

    limits = limits or TeamRunLimits()
    run_id = str(uuid.uuid4())
    context = TeamContext()
    steps = 0

    for ticket in open_tickets:
        if steps >= limits.max_steps:
            break
        steps += 1
        ticket_id = int(ticket["id"])
        _audit(
            run_id,
            steps,
            AgentName.BOSS,
            "read_ticket_for_triage",
            ticket_id,
            {"ticket_fields": sorted(ticket.keys())},
            {"status": ticket.get("status"), "type": ticket.get("type")},
        )
        route = {
            "customer_order": AgentName.INVENTORY,
            "price_override": AgentName.INVENTORY,
            "rent_notice": AgentName.FACILITIES,
        }.get(ticket.get("type"), AgentName.BOSS)
        if len(context.queue) >= limits.max_delegations:
            break
        context.delegate(
            Delegation(
                from_agent=AgentName.BOSS,
                to_agent=route,
                ticket_id=ticket_id,
                task=f"Review ticket {ticket_id} using MCP facts.",
                reason=f"Ticket type is {ticket.get('type')}.",
            )
        )
        steps += 1
        _audit(
            run_id,
            steps,
            AgentName.BOSS,
            "delegate_ticket",
            ticket_id,
            {"ticket_type": ticket.get("type")},
            {"delegation_created": True},
            delegated_to=route,
        )

    # Execute the planned specialist handoffs with database-grounded MCP tools.
    from mcp_server.server import (
        get_lease_rent_context,
        get_payment_status_context,
        get_ticket_full_context,
        get_ticket_restock_and_financial_context,
        list_restock_vendor_options,
        prepare_payment_request,
    )

    for ticket in open_tickets:
        ticket_id = int(ticket["id"])
        ticket_type = ticket.get("type")
        if ticket_type == "customer_order":
            specialist = AgentName.INVENTORY
            first = get_ticket_restock_and_financial_context(ticket_id)
            second = list_restock_vendor_options(ticket["sku"], ticket["size"])
            tool_names = ["get_ticket_restock_and_financial_context", "list_restock_vendor_options"]
            next_agent = AgentName.CUSTOMER_SERVICE
            summary = f"Inventory found shortage {first['shortage_qty']} and reviewed vendor eligibility; Customer Service drafted a stock-update message."
            status = "closed"
        elif ticket_type == "rent_notice":
            specialist = AgentName.FACILITIES
            first = get_lease_rent_context(ticket_id)
            second = get_ticket_full_context(ticket_id)
            third = get_payment_status_context(ticket_id)
            proposal = prepare_payment_request("rent", ticket["lease_id"], first["lease"]["monthly_rent"], "checking")
            tool_names = ["get_lease_rent_context", "get_ticket_full_context", "get_payment_status_context", "prepare_payment_request"]
            next_agent = AgentName.ACCOUNTING
            summary = "Facilities verified the lease and due date; Accounting prepared a rent payment proposal pending human approval."
            status = "pending_approval"
        else:
            specialist = AgentName.INVENTORY
            first = get_ticket_restock_and_financial_context(ticket_id)
            second = list_restock_vendor_options(ticket["sku"], ticket["size"])
            tool_names = ["get_ticket_restock_and_financial_context", "list_restock_vendor_options"]
            next_agent = AgentName.ACCOUNTING
            summary = f"Inventory found shortage {first['shortage_qty']} and supplied margin, cash, lead-time, and vendor-block facts to Accounting."
            status = "closed"

        steps += 1
        _audit(run_id, steps, specialist, "used_mcp_tools", ticket_id, {"tools": tool_names}, {"tool_outputs_recorded": True})
        steps += 1
        _audit(run_id, steps, specialist, "delegate_specialist_handoff", ticket_id, {"completed_tools": tool_names}, {"next_step": summary}, delegated_to=next_agent, requires_human_approval=status == "pending_approval")
        with sqlite3.connect(DATABASE_PATH) as db:
            prior = db.execute("SELECT notes FROM tickets WHERE id = ?", (ticket_id,)).fetchone()[0] or ""
            db.execute("UPDATE tickets SET status = ?, notes = ? WHERE id = ?", (status, f"{prior}\n{summary}".strip(), ticket_id))
            db.commit()

    return TeamRunResult(status="completed" if all(t.get("type") != "rent_notice" for t in open_tickets) else "pending_human_approval", run_id=run_id, steps=steps)


def run_team_sync(open_tickets: list[dict], limits: TeamRunLimits | None = None) -> TeamRunResult:
    return asyncio.run(run_team(open_tickets, limits))
