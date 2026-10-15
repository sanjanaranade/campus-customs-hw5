"""Accounting agent: cash, invoices, margins, and payment proposals."""

from .agent_common import make_agent
from .models import AgentName

accounting_agent = make_agent(AgentName.ACCOUNTING)
