
import asyncio
import os
import sys
from contextlib import AsyncExitStack
from typing import Any, Dict, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class LocalMCPClient:
    def __init__(self):
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._exit_stack: Optional[AsyncExitStack] = None
        self._session: Optional[ClientSession] = None

    def _ensure_loop(self) -> asyncio.AbstractEventLoop:
        if self._loop and not self._loop.is_closed():
            return self._loop
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        return self._loop

    def start(self) -> None:
        loop = self._ensure_loop()
        loop.run_until_complete(self._astart())

    async def _astart(self) -> None:
        if self._session:
            return

        # Project root: .../map-agent-project
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

        self._exit_stack = AsyncExitStack()

        server_params = StdioServerParameters(
            # Use the current venv python
            command=sys.executable,
            # Run the MCP server module
            args=["-m", "app.mcp_local.mcp_server"],
            # Ensure server can import `app.*`
            env={**os.environ, "PYTHONPATH": project_root},
            # Ensure relative paths resolve from repo root
            cwd=project_root,
        )

        stdio, write = await self._exit_stack.enter_async_context(stdio_client(server_params))
        self._session = await self._exit_stack.enter_async_context(ClientSession(stdio, write))
        await self._session.initialize()

    def call(self, tool_name: str, args: Dict[str, Any]) -> Any:
        if not self._session:
            self.start()
        loop = self._ensure_loop()
        result = loop.run_until_complete(self._session.call_tool(tool_name, args))

        # Convert to plain dict
        data = result.model_dump()

        # Try to unwrap JSON returned as a text content block
        content = data.get("content") or []
        if content and isinstance(content, list):
            first = content[0]
            if isinstance(first, dict) and "text" in first:
                import json
                try:
                    return json.loads(first["text"])
                except Exception:
                    return {"ok": True, "text": first["text"], "_raw": data}

        return data


