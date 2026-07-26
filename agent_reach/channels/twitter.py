# -*- coding: utf-8 -*-
"""Twitter/X — check if twitter-cli or bird CLI is available."""

from .base import Channel
from agent_reach.probe import probe_command


class TwitterChannel(Channel):
    name = "twitter"
    description = "Twitter/X "
    backends = ["twitter-cli", "OpenCLI", "bird CLI (legacy)"]
    tier = 1

    def can_handle(self, url: str) -> bool:
        from urllib.parse import urlparse
        d = urlparse(url).netloc.lower()
        return "x.com" in d or "twitter.com" in d

    def check(self, config=None):
        """Probe candidates in order; first fully-usable backend wins.

        :status, ok ;
        no ok  warn——"not logged in" twitter-cli
        ,fully available OpenCLI .
        """
        self.active_backend = None
        findings = []

        for backend in self.ordered_backends(config):
            if backend == "twitter-cli":
                result = self._check_twitter_cli()
            elif backend == "OpenCLI":
                result = self._check_opencli()
            elif backend == "bird CLI (legacy)":
                result = self._check_bird()
            else:
                continue

            if result is None:
                continue  # not installed——
            findings.append((backend, *result))

        for wanted in ("ok", "warn"):
            for backend, status, message in findings:
                if status == wanted:
                    self.active_backend = backend
                    return status, message

        if findings:  #  broken/timeout 
            return "error", "\n".join(m for _, _, m in findings)

        return "warn", (
            "Twitter CLI not installed.install:\n"
            "  pipx install twitter-cli\n"
            ":\n"
            "  uv tool install twitter-cli"
        )

    def _check_twitter_cli(self):
        """ twitter-cli. None not installed, (status, message).

        `twitter status` :log in "ok: true",
        not logged in "not_authenticated"——Tool,
         probe  error status output .
        """
        probe = probe_command(
            "twitter", ["status"], timeout=15, retries=1, package="twitter-cli"
        )
        if probe.status == "missing":
            return None
        if probe.status == "broken":
            return "error", "twitter-cli command exists butcannot execute.\n" + probe.hint
        if probe.status == "timeout":
            return "error", "twitter-cli health check timed out( 1 ).\n" + probe.hint

        output = probe.output
        if "ok: true" in output:
            return "ok", (
                "twitter-cli fully available(search,,,/Article,"
                "users,Thread)"
            )
        if "not_authenticated" in output:
            return "warn", (
                "twitter-cli is installed but not authenticated.:\n"
                "  export TWITTER_AUTH_TOKEN=\"xxx\"\n"
                "  export TWITTER_CT0=\"yyy\"\n"
                "browserlog in x.com"
            )
        return "warn", (
            "twitter-cli installauthenticationfailed.run:\n"
            "  twitter -v status "
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
                "opencli twitter search/article/user-posts -f yaml"
            )
        return "warn", st.hint

    def _check_bird(self):
        """ bird/birdx(legacy ). None not installed, (status, message)."""
        last_failure = None
        for cmd in ("bird", "birdx"):
            probe = probe_command(
                cmd, ["check"], timeout=15, retries=1, package="@steipete/bird"
            )
            if probe.status == "missing":
                continue
            if probe.status == "broken":
                last_failure = (
                    "error",
                    f"{cmd} command exists butcannot execute(bird  npm ,available "
                    "npm install -g @steipete/bird reinstall).\n" + probe.hint,
                )
                continue  # bird  birdx
            if probe.status == "timeout":
                last_failure = (
                    "error",
                    f"{cmd} health check timed out( 1 ).\n" + probe.hint,
                )
                continue

            output = probe.output
            if probe.ok:
                return "ok", "bird CLI available(read,search,/X Article)"
            if "Missing credentials" in output or "missing" in output.lower():
                return "warn", (
                    "bird CLI installauthentication is not configured.:\n"
                    "  export AUTH_TOKEN=\"xxx\"\n"
                    "  export CT0=\"yyy\""
                )
            return "warn", (
                "bird CLI installauthenticationfailed."
            )
        return last_failure
