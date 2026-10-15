"""Runtime configuration; secrets are read from environment variables only."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_DIR = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_DIR / ".env")
DATABASE_PATH = Path(
    os.getenv("CAMPUS_CUSTOMS_DB", str(PROJECT_DIR / "data" / "campus_customs_new.db"))
)
AUDIT_PATH = PROJECT_DIR / "output" / "audit_trail.json"
MODEL_NAME = "gpt-6-luna"
PORTKEY_BASE_URL = "https://api.portkey.ai/v1"


def portkey_api_key() -> str:
    key = os.getenv("PORTKEY_API_KEY")
    if not key:
        raise RuntimeError("PORTKEY_API_KEY is required for model calls")
    return key
