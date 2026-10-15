"""Boss agent: triage and final decisions."""

from .agent_common import make_agent
from .models import AgentName

boss_agent = make_agent(AgentName.BOSS)
