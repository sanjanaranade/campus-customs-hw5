"""PydanticAI model configuration for Portkey."""

from __future__ import annotations

from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

from .config import MODEL_NAME, PORTKEY_BASE_URL, portkey_api_key


def gpt_luna_model() -> OpenAIChatModel:
    """Return the only permitted model for this assignment."""

    return OpenAIChatModel(
        MODEL_NAME,
        provider=OpenAIProvider(
            api_key=portkey_api_key(),
            base_url=PORTKEY_BASE_URL,
        ),
    )
