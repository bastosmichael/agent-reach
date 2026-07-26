# -*- coding: utf-8 -*-
"""Exa Search — check if mcporter + Exa MCP is available."""

from agent_reach.probe import probe_command

from .base import Channel

#: mcporter  npm ,broken link pipx/uv 
_MCPORTER_BROKEN_HINT = "mcporter cannot execute(node ),reinstall:\n  npm install -g mcporter"


class ExaSearchChannel(Channel):
    name = "exa_search"
    description = "web semantic search"
    backends = ["Exa via mcporter"]
    tier = 0

    def can_handle(self, url: str) -> bool:
        return False  # Search-only channel

    def check(self, config=None):
        self.active_backend = None
        probe = probe_command("mcporter", ["config", "list"], timeout=10, package="mcporter")
        if probe.status == "missing":
            return "off", (
                "requires mcporter + Exa MCP.install:\n"
                "  npm install -g mcporter\n"
                "  mcporter config add exa https://mcp.exa.ai/mcp"
            )
        if probe.status == "broken":
            return "error", _MCPORTER_BROKEN_HINT
        if not probe.ok:  # timeout / error
            return "error", f"mcporter exception:{probe.hint or probe.output or probe.status}"
        if "exa" in probe.output.lower():
            self.active_backend = self.backends[0]
            return "ok", "web semantic searchavailable(free, API Key)"
        return "off", (
            "mcporter  Exa not configured.run:\n"
            "  mcporter config add exa https://mcp.exa.ai/mcp"
        )
