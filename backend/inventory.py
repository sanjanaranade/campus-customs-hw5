"""Inventory agent: stock, shortages, and vendor restock facts."""

from .agent_common import make_agent
from .models import AgentName

inventory_agent = make_agent(AgentName.INVENTORY)
