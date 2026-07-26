# -*- coding: utf-8 -*-
"""Reddit — multi-backend: OpenCLI / rdt-cli. Login is mandatory.

Honest tiering (live-verified 2026-06): there is NO zero-config path.
Anonymous .json endpoints are blocked (403 anti-bot, all variants), and
the official API closed self-service registration in 2025-11 (manual
approval, individual scripts rarely granted — PRAW is only an option for
users who already hold credentials). Every working backend rides a
logged-in session: OpenCLI reuses the browser's, rdt-cli imports cookies.
"""

import json
import shutil
import subprocess

from agent_reach.utils.process import utf8_subprocess_env

from .base import Channel

_CREDENTIAL_FILE = "~/.config/rdt-cli/credential.json"
# Pinned to the 0.4.2 state — PyPI still only has 0.4.1 (upstream issue #10).
_RDT_GIT_SOURCE = "git+https://github.com/public-clis/rdt-cli.git@5e4fb3720d5c174e976cd425ccc3b879d52cac66"

#: shell "/"( agent_reach.probe)
_BROKEN_EXIT_CODES = (126, 127)

#: rdt  git install(PyPI ),broken link probe  pipx/uv 
_RDT_BROKEN_HINT = (
    "rdt command exists butcannot execute—— Python  venv .\n"
    "PyPI ,recommended git reinstall:\n"
    f"  pipx install --force '{_RDT_GIT_SOURCE}'"
)


class RedditChannel(Channel):
    name = "reddit"
    description = "Reddit postscomments"
    backends = ["OpenCLI", "rdt-cli"]
    tier = 1  # no zero-config path exists — see module docstring

    def can_handle(self, url: str) -> bool:
        from urllib.parse import urlparse

        d = urlparse(url).netloc.lower()
        return "reddit.com" in d or "redd.it" in d

    def check(self, config=None):
        """Probe candidates in order; first fully-usable backend wins."""
        self.active_backend = None
        findings = []

        for backend in self.ordered_backends(config):
            if backend == "OpenCLI":
                result = self._check_opencli()
            else:
                result = self._check_rdt()
            if result is None:
                continue
            findings.append((backend, *result))

        for wanted in ("ok", "warn"):
            for backend, status, message in findings:
                if status == wanted:
                    self.active_backend = backend
                    return status, message

        if findings:
            return "error", "\n".join(m for _, _, m in findings)

        return "off", (
            "not installedany Reddit .:Reddit noconfigure"
            "( .json , API ),mustlogin session.recommended:\n"
            "  :agent-reach install --channels opencli\n"
            "       ( Chrome login session,log in reddit.com available)\n"
            f"  /:pipx install '{_RDT_GIT_SOURCE}'\n"
            "        `rdt login`  Cookie( doctor )\n"
            "Mainland Chinaaccess Reddit requiresproxy"
        )

    def _check_opencli(self):
        """OpenCLI candidate. None = not installed."""
        from agent_reach.backends import opencli_status

        st = opencli_status()
        if not st.installed:
            return None
        if st.broken:
            return "error", st.hint
        if st.ready:
            return "ok", (
                "OpenCLI available(reuse browserlogin session).:"
                "opencli reddit search/read/subreddit/hot -f yaml"
            )
        return "warn", st.hint

    def _check_rdt(self):
        """rdt-cli candidate. None = not installed."""
        rdt = shutil.which("rdt")
        if not rdt:
            return None

        #  probe_command: `rdt status --json` (rc=0) stderr
        # ,probe  stdout+stderr  JSON .
        #  subprocess(stdout ),exception probe :
        # exec failed/126/127 → broken(venv broken link),TimeoutExpired → .
        try:
            r = subprocess.run(
                [rdt, "status", "--json"],
                capture_output=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
                env=utf8_subprocess_env(),
            )
        except subprocess.TimeoutExpired:
            return "error", "rdt (>10s),Reddit status unknown.retry laterrun `rdt status` view details"
        except OSError:
            #  FileNotFoundError:which  exec failed = venv broken link(probe  broken)
            return "error", _RDT_BROKEN_HINT

        if r.returncode in _BROKEN_EXIT_CODES:
            return "error", _RDT_BROKEN_HINT

        if r.returncode != 0:
            detail = (r.stderr or r.stdout or "").strip().splitlines()
            tail = detail[-1] if detail else "no output"
            return "error", f"rdt exception(exit {r.returncode}):{tail}.run `rdt status` view details"

        #  → rdt (log in)
        try:
            data = json.loads(r.stdout or "")
        except json.JSONDecodeError:
            data = None
        if not isinstance(data, dict):
            return "warn", "rdt-cli availablestatus,run `rdt status` log instatus"

        info = data.get("data")
        if not isinstance(info, dict):
            info = {}
        authenticated = info.get("authenticated", False)
        username = info.get("username") or ""

        if authenticated:
            suffix = f"(log in:{username})" if username else ""
            return "ok", (
                f"rdt-cli available{suffix}(searchposts,,comments;"
                " 2026-03 ,users OpenCLI)"
            )

        return "warn", (
            "rdt-cli installnot logged in.Reddit  2024 authentication,"
            "not logged in 403.\n\n"
            "():run `rdt login`\n"
            "  browserlog in reddit.com,run Cookie.\n\n"
            "(, Chrome/Edge 127+ ):\n"
            "  1. Chrome install Cookie-Editor :\n"
            "     https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm\n"
            "  2. browser reddit.com(log in)\n"
            "  3.  Cookie-Editor , `reddit_session`, Value\n"
            f"  4.  {_CREDENTIAL_FILE}:\n"
            '     {"cookies": {"reddit_session": "< Value>"}, '
            '"source": "manual", "username": "<users>", '
            '"modhash": null, "saved_at": 0, "last_verified_at": null}\n\n'
            ":`rdt status --json`  authenticated: true"
        )
