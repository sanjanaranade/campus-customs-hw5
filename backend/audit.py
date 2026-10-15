"""Append-only audit trail for every agent-loop step."""

from __future__ import annotations

import json
from pathlib import Path
from threading import Lock

from .config import AUDIT_PATH
from .models import AuditEvent


_LOCK = Lock()


def append_audit_event(event: AuditEvent, path: Path = AUDIT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with _LOCK:
        if path.exists():
            try:
                events = json.loads(path.read_text())
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"Audit file is not valid JSON: {path}") from exc
            if not isinstance(events, list):
                raise RuntimeError("Audit trail must contain a JSON list")
        else:
            events = []
        events.append(event.model_dump(mode="json"))
        path.write_text(json.dumps(events, indent=2) + "\n")
