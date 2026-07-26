# Changelog / Changelog

All notable changes to this project will be documented in this file.

file.

---

## [1.3.1] - 2026-03-27

### 🐛 Bug Fixes / Fixes

#### 📈 Xueqiu (Xueqiu) — Fixes

- **Fixes 400 Cause:** `_ensure_cookies()` accessget `acw_tc`( DDoS token),`xq_a_token` Xueqiu JS , HTTP get. cookie :1 read config file(`--from-browser` save)→ 2  Chrome browser(install browser-cookie3)→ 3 homepage fallback
- **Fixes User-Agent:** `"agent-reach/1.0"` Xueqiu, Chrome UA
- **Fixes `Referer` :**  API  `Referer: https://xueqiu.com/`
- **Fixes `get_hot_posts()` :**  `/statuses/hot/listV3.json` ( body), `/v4/statuses/public_timeline_by_category.json`, `item.data` JSON get author/likes/text
- **Fixes `urllib.request.quote` → `urllib.parse.quote`:** 
- **Fixes `configure --from-browser` Xueqiu Cookie:** `PLATFORM_SPECS`  Xueqiu, `xq_a_token` save
- **:** README/SKILL.md "configure"/"public API, no login required" → requires browser cookie
- **:** `check()` failed `configure --from-browser chrome` "a proxy may be required"

---

## [1.3.0] - 2026-03-12

### 🆕 New Channels / New Channels

#### 💻 V2EX
- Hot topics, node topics, topic detail + replies, user profile via public JSON API
- Zero config — no auth, no proxy, no API key required
- `get_hot_topics(limit)`, `get_node_topics(node_name, limit)`, `get_topic(id)`, `get_user(username)`
-  JSON API gettrendingposts,nodesposts,postsdetails+replies,user information
- configure,authentication,proxy, API Key

### 📈 Improvements / Improvements

- Channel count: 14 → 15
- :14 → 15

---

## [1.1.0] - 2025-02-25

### 🆕 New Channels / New Channels

#### ~~📷 Instagram~~ (removed — upstream blocked)
- ~~Read public posts and profiles via [instaloader](https://github.com/instaloader/instaloader)~~
- **Removed:** Instagram's aggressive anti-scraping measures broke all available open-source tools (instaloader, etc.). See [instaloader#2585](https://github.com/instaloader/instaloader/issues/2585). Will re-add when upstream recovers.
- **:** Instagram Tool(instaloader )..

#### 💼 LinkedIn
- Read person profiles, company pages, and job details via [linkedin-scraper-mcp](https://github.com/stickerdaniel/linkedin-mcp-server)
- Search people and jobs via MCP, with Exa fallback
- Fallback to Jina Reader when MCP is not configured
-  linkedin-scraper-mcp read Profile,company,jobsdetails
-  MCP searchtalentjobs,Exa 
- not configured MCP  fallback  Jina Reader

#### 🏢 Boss
- QR code login via [mcp-bosszp](https://github.com/mucsbr/mcp-bosszp)
- Job search and recruiter greeting via MCP
- Fallback to Jina Reader for reading job pages
-  mcp-bosszp scan QR codelog in
- MCP searchjobs, HR 
- Jina Reader readjobs

### 📈 Improvements / Improvements

- Channel count: 9 → 12
- `agent-reach doctor` now detects all 12 channels
- CLI: added `search-linkedin`, `search-bosszhipin` subcommands
- Updated install guide with setup instructions for new channels
- :9 → 11
- `agent-reach doctor`  11 
- CLI: `search-linkedin`,`search-bosszhipin` 
- installNew Channelsconfigure

---

## [1.0.0] - 2025-02-24

### 🎉 Initial Release / 

- 9 channels: Web, Twitter/X, YouTube, Bilibili, GitHub, Reddit, XiaoHongShu, RSS, Exa Search
- CLI with `read`, `search`, `doctor`, `install` commands
- Unified channel interface — each platform is a single pluggable Python file
- Auto-detection of local vs server environments
- Built-in diagnostics via `agent-reach doctor`
- Skill registration for Claude Code / OpenClaw / Cursor
- 9 :web page,Twitter/X,YouTube,Bilibili,GitHub,Reddit,Xiaohongshu,RSS,Exa search
- CLI  `read`,`search`,`doctor`,`install` 
-  —  Python file
- /
-  `agent-reach doctor`
- Skill  Claude Code / OpenClaw / Cursor
