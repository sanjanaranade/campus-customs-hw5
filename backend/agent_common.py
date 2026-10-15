"""Shared PydanticAI agent construction and team delegation context."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic_ai import Agent

from .model_provider import gpt_luna_model
from .models import AgentName, Delegation


PROMPTS_DIR = Path(__file__).parent / "prompts"


def prompt_for(agent: AgentName) -> str:
    return (PROMPTS_DIR / f"{agent.value}.txt").read_text()


def make_agent(agent: AgentName) -> Agent:
    return Agent(
        gpt_luna_model(),
        name=agent.value,
        instructions=prompt_for(agent),
        retries=1,
    )


class TeamContext:
    """Shared context allowing any agent to delegate to any other agent."""

    def __init__(self) -> None:
        self.queue: list[Delegation] = []
        self.results: dict[str, Any] = {}

    def delegate(self, delegation: Delegation) -> None:
        self.queue.append(delegation)

    def record(self, key: str, value: Any) -> None:
        self.results[key] = value
