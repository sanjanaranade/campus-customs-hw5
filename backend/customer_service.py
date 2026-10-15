"""Customer-service agent: drafts, never sends, messages."""

from .agent_common import make_agent
from .models import AgentName

customer_service_agent = make_agent(AgentName.CUSTOMER_SERVICE)
