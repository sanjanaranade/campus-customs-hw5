"""Typed contracts shared by the Campus Customs agent team."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class AgentName(str, Enum):
    BOSS = "boss"
    INVENTORY = "inventory"
    ACCOUNTING = "accounting"
    FACILITIES = "facilities"
    CUSTOMER_SERVICE = "customer_service"


class TicketRef(BaseModel):
    ticket_id: int = Field(gt=0)


class Delegation(BaseModel):
    from_agent: AgentName
    to_agent: AgentName
    ticket_id: int = Field(gt=0)
    task: str = Field(min_length=1, max_length=1000)
    reason: str = Field(min_length=1, max_length=2000)


class AgentFinding(BaseModel):
    agent: AgentName
    ticket_id: int = Field(gt=0)
    summary: str = Field(min_length=1, max_length=4000)
    facts: dict[str, Any] = Field(default_factory=dict)
    recommended_next_step: str = Field(min_length=1, max_length=2000)
    requires_human_approval: bool = False


class AuditEvent(BaseModel):
    event_id: str
    timestamp: datetime
    run_id: str
    step: int = Field(gt=0)
    event_type: str
    agent: AgentName
    ticket_id: int | None = None
    action: str
    input_summary: dict[str, Any] = Field(default_factory=dict)
    output_summary: dict[str, Any] = Field(default_factory=dict)
    delegated_to: AgentName | None = None
    requires_human_approval: bool = False


class PaymentProposal(BaseModel):
    kind: str
    ref_id: int
    amount: float = Field(gt=0)
    account: str
    reason: str
    requires_human_approval: bool = True


class TeamRunLimits(BaseModel):
    max_steps: int = Field(default=24, ge=1, le=50)
    max_delegations: int = Field(default=12, ge=0, le=30)
    max_model_calls: int = Field(default=12, ge=0, le=30)
    max_output_tokens_per_call: int = Field(default=1200, ge=128, le=3000)


class TeamRunResult(BaseModel):
    run_id: str
    status: str
    steps: int
    findings: list[AgentFinding] = Field(default_factory=list)
    pending_approvals: list[PaymentProposal] = Field(default_factory=list)
