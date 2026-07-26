# -*- coding: utf-8 -*-
"""GitHub — check if gh CLI is available."""

from agent_reach.probe import probe_command

from .base import Channel


class GitHubChannel(Channel):
    name = "github"
    description = "GitHub repositorycode"
    backends = ["gh CLI"]
    tier = 0

    def can_handle(self, url: str) -> bool:
        from urllib.parse import urlparse
        return "github.com" in urlparse(url).netloc.lower()

    def check(self, config=None):
        #  gh auth status .:not logged in rc!=0 (warn), error.
        probe = probe_command("gh", ["auth", "status"], timeout=10, package="gh")
        if probe.status == "missing":
            self.active_backend = None
            return "warn", "gh CLI not installed.install:https://cli.github.com"
        if probe.status == "broken":
            # gh install(brew/), pip —— pipx/uv 
            self.active_backend = None
            return "error", (
                "gh command exists butcannot execute——install.reinstallFixes:\n"
                "  brew reinstall gh\n"
                " https://cli.github.com install gh CLI"
            )
        if probe.status == "timeout":
            # gh (Tool),status
            self.active_backend = "gh CLI"
            return "warn", "gh CLI status,run gh auth status view details"
        if probe.ok:
            self.active_backend = "gh CLI"
            return "ok", "fully available(read,search,Fork,Issue,PR )"
        # rc != 0:gh not authenticated(gh auth status )
        self.active_backend = "gh CLI"
        return "warn", "gh CLI is installed but not authenticated.run gh auth login "
