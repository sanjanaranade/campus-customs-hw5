"""Async client used by the backend agents to reach the local MCP server."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from fastmcp import Client


PROJECT_DIR = Path(__file__).resolve().parents[1]
SERVER = {
    "mcpServers": {
        "campus-customs": {
            "command": str(PROJECT_DIR / ".venv" / "bin" / "python"),
            "args": [str(PROJECT_DIR / "mcp_server" / "server.py")],
        }
    }
}


async def call_tool(name: str, arguments: dict[str, Any] | None = None) -> Any:
    """Call one local MCP tool and return its structured result."""

    async with Client(SERVER) as client:
        result = await client.call_tool(name, arguments or {})
        return result.data
