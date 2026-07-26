# -*- coding: utf-8 -*-
"""V2EX — public API channel for topics, nodes, users, and replies."""

import json
import urllib.request
from typing import Any
from .base import Channel

_UA = "agent-reach/1.0"
_TIMEOUT = 10


def _get_json(url: str) -> Any:
    """Fetch *url* and return parsed JSON. Raises on HTTP/network errors."""
    req = urllib.request.Request(url, headers={"User-Agent": _UA})
    with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


class V2EXChannel(Channel):
    name = "v2ex"
    description = "V2EX nodes,topicsreplies"
    backends = ["V2EX API (public)"]
    tier = 0

    # ------------------------------------------------------------------ #
    # URL routing
    # ------------------------------------------------------------------ #

    def can_handle(self, url: str) -> bool:
        from urllib.parse import urlparse
        d = urlparse(url).netloc.lower()
        return "v2ex.com" in d

    # ------------------------------------------------------------------ #
    # Health check
    # ------------------------------------------------------------------ #

    def check(self, config=None):
        try:
            _get_json(
                "https://www.v2ex.com/api/topics/show.json?node_name=python&page=1"
            )
            self.active_backend = self.backends[0]
            return "ok", "public API is available(trendingtopics,nodes,topicsdetails,user information)"
        except Exception as e:
            self.active_backend = None
            return "warn", f"V2EX API failed(a proxy may be required):{e}"

    # ------------------------------------------------------------------ #
    # Data-fetching methods
    # ------------------------------------------------------------------ #

    def get_hot_topics(self, limit: int = 20) -> list:
        """gettrendingposts.

        Returns a list of dicts with keys:
          title, url, replies, node_name, node_title, content
        """
        data = _get_json("https://www.v2ex.com/api/topics/hot.json")
        results = []
        for item in data[:limit]:
            node = item.get("node") or {}
            content = item.get("content", "") or ""
            results.append(
                {
                    "id": item.get("id", 0),
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "replies": item.get("replies", 0),
                    "node_name": node.get("name", ""),
                    "node_title": node.get("title", ""),
                    "content": content[:200],
                    "created": item.get("created", 0),
                }
            )
        return results

    def get_node_topics(self, node_name: str, limit: int = 20) -> list:
        """getnodesposts.

        Args:
            node_name: nodes, "python","tech","jobs"
            limit:     maximum number of results

        Returns a list of dicts with keys:
          title, url, replies, node_name, node_title, content
        """
        url = (
            f"https://www.v2ex.com/api/topics/show.json"
            f"?node_name={node_name}&page=1"
        )
        data = _get_json(url)
        results = []
        for item in data[:limit]:
            node = item.get("node") or {}
            content = item.get("content", "") or ""
            results.append(
                {
                    "id": item.get("id", 0),
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "replies": item.get("replies", 0),
                    "node_name": node.get("name", node_name),
                    "node_title": node.get("title", ""),
                    "content": content[:200],
                    "created": item.get("created", 0),
                }
            )
        return results

    def get_topic(self, topic_id: int) -> dict:
        """getpostsdetailsreplies.

        Args:
            topic_id: posts ID( URL https://www.v2ex.com/t/<id> get)

        Returns a dict with keys:
          id, title, url, content, replies_count, node_name, node_title,
          author, created, replies (list of dicts with: author, content, created)
        """
        topic_data = _get_json(
            f"https://www.v2ex.com/api/topics/show.json?id={topic_id}"
        )
        # API returns a list even for single-ID queries
        if isinstance(topic_data, list):
            topic = topic_data[0] if topic_data else {}
        else:
            topic = topic_data

        node = topic.get("node") or {}
        member = topic.get("member") or {}

        # Fetch replies (first page)
        try:
            replies_raw = _get_json(
                f"https://www.v2ex.com/api/replies/show.json"
                f"?topic_id={topic_id}&page=1"
            )
        except Exception:
            replies_raw = []

        replies = [
            {
                "author": (r.get("member") or {}).get("username", ""),
                "content": r.get("content", ""),
                "created": r.get("created", 0),
            }
            for r in (replies_raw or [])
        ]

        return {
            "id": topic.get("id", topic_id),
            "title": topic.get("title", ""),
            "url": topic.get("url", f"https://www.v2ex.com/t/{topic_id}"),
            "content": topic.get("content", ""),
            "replies_count": topic.get("replies", 0),
            "node_name": node.get("name", ""),
            "node_title": node.get("title", ""),
            "author": member.get("username", ""),
            "created": topic.get("created", 0),
            "replies": replies,
        }

    def get_user(self, username: str) -> dict:
        """getuser information.

        Args:
            username: V2EX users

        Returns a dict with keys:
          id, username, url, website, twitter, psn, github, btc,
          location, bio, avatar, created
        """
        data = _get_json(
            f"https://www.v2ex.com/api/members/show.json?username={username}"
        )
        return {
            "id": data.get("id", 0),
            "username": data.get("username", username),
            "url": data.get("url", f"https://www.v2ex.com/member/{username}"),
            "website": data.get("website", ""),
            "twitter": data.get("twitter", ""),
            "psn": data.get("psn", ""),
            "github": data.get("github", ""),
            "btc": data.get("btc", ""),
            "location": data.get("location", ""),
            "bio": data.get("bio", ""),
            "avatar": data.get("avatar_large", data.get("avatar_normal", "")),
            "created": data.get("created", 0),
        }

    def search(self, query: str, limit: int = 10) -> list:
        """searchposts.

        :V2EX  API search(/api/search.json available).
         Jina Reader proxy V2EX searchget(plain text,data).

        search,access https://www.v2ex.com/?q=<query> 
         Exa channel  site:v2ex.com search.

        Returns:
            list of dicts with keys: title, url, snippet
            Ifsearchavailable, {"error": str} .
        """
        return [
            {
                "error": (
                    "V2EX  API search."
                    f":https://www.v2ex.com/?q={query} "
                    " Exa channel  site:v2ex.com search."
                )
            }
        ]
