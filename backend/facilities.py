"""Facilities agent: leases, rent, and shop-space obligations."""

from .agent_common import make_agent
from .models import AgentName

facilities_agent = make_agent(AgentName.FACILITIES)
