# Agent Reach — Installation Guide

## For Humans

Copy this to your AI Agent:

```
Help me install Agent Reach:https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
```

> 🛡️ **Security-conscious?** Use safe mode — it won't auto-install system packages:
> ```
> Help me install Agent Reach(safe mode):https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/install.md
> Use the --safe flag during installation
> ```

---

## For AI Agents

### Goal

Install Agent Reach and all upstream tools so your user's agent has full internet access. After installation, you'll use the upstream tools directly (OpenCLI, twitter-cli, bili-cli, rdt-cli, yt-dlp, mcporter, gh CLI, etc.) — Agent Reach is the selector, installer, health checker and router, never a wrapper.

### ⚠️ Boundaries

When fixing issues, stay within these limits:

- **DO NOT** run commands with `sudo` unless the user explicitly approved
- **DO NOT** modify system files outside `~/.agent-reach/`
- **DO NOT** install packages not listed in this guide
- **DO NOT** disable firewalls, security settings, or system protections
- **DO NOT** clone repos, create files, or run commands inside the agent workspace / working directory
- If something requires elevated permissions, **tell the user** what's needed and let them decide

### 📁 Directory Rules

All Agent Reach files go in dedicated directories — **never in the agent workspace**:

| Purpose | Directory | Example |
|---------|-----------|---------|
| Config & tokens | `~/.agent-reach/` | `~/.agent-reach/config.json` |
| Upstream tool repos | `~/.agent-reach/tools/` | `~/.agent-reach/tools/xiaoyuzhou/` |
| Temporary files | `/tmp/` | `/tmp/yt-dlp-output/` |
| Skills | `~/.openclaw/skills/agent-reach/` | SKILL.md |

**Why?** If you clone repos or create files in the workspace, it pollutes the user's project directory and can break their agent over time. Keep the workspace clean.

### Step 1: Install the basics

```bash
# recommended:pipx()
pipx install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto

# If Python  Homebrew /  PEP 668(externally-managed-environment)
# install:
python3 -m venv ~/.agent-reach-venv
source ~/.agent-reach-venv/bin/activate
pip install https://github.com/Panniantong/agent-reach/archive/main.zip
agent-reach install --env=auto
```

> 💡 **Windows / Microsoft Store Python alias?**
> If `python3 --version`  Microsoft Store, `where python3` 
> `...\AppData\Local\Microsoft\WindowsApps\python3.exe`, `python3`  Windows
>  Store alias,available Python install. Python Launcher `py -3`,installdirectory `python.exe`.
>
> PowerShell :
> ```powershell
> py -3 -m venv $env:USERPROFILE\.agent-reach-venv
> $env:USERPROFILE\.agent-reach-venv\Scripts\Activate.ps1
> python -m pip install https://github.com/Panniantong/agent-reach/archive/main.zip
> agent-reach install --env=auto
> ```

This installs core infrastructure (gh CLI, Node.js, mcporter, Exa search, yt-dlp config) and activates these zero-config channels:

- Web (Jina Reader), YouTube, GitHub, RSS, Exa Search, V2EX, Bilibili (basic)

> 💡 **macOS / Homebrew Python  `externally-managed-environment`?**
>  PEP 668 , Agent Reach . `pipx install ...`, `venv` install.

**Safe mode / Dry run:**

```bash
agent-reach install --env=auto --safe      # Check only, no auto-install
agent-reach install --env=auto --dry-run   # Preview what would be done
```

### Step 2: Ask the user which optional channels they want

After installing the basics, **ask the user** which additional channels they need. Present this list:

> The base channels are installed!You can now ask me to search the web, watch YouTube, read GitHub, and more.
>
> These optional channels are also available; which ones do you need?
>
> - 🌟 **OpenCLI**(recommended on desktop)— one installation,Xiaohongshu/Reddit/Facebook/Instagram/Bilibilisubtitles/Twitter unlocks all(reuse browserlogin session,configure; Chrome "Add extension")
> - 🐦 **Twitter/X** — ,(requireslog in Cookie)
> - 📈 **Xueqiu** — stock quotes,trendingposts(requireslog in Cookie)
> - 🎙️ **Xiaoyuzhou Podcast** — audio to text(requiresfree Groq Key)
> - 📕 **Xiaohongshu** — search,,comments( OpenCLI; xiaohongshu-mcp scan QR code)
> - 📖 **Reddit** — searchposts(mustlogin session: OpenCLI  rdt-cli + Cookie)
> - 📘 **Facebook** — search,,Feed,( OpenCLI, Chrome login session)
> - 📷 **Instagram** — userssearch,Profile,usersposts,Explore( OpenCLI, Chrome login session)
> - 📺 **Bilibili** — trending,,search,videodetails(bili-cli,no login required)
> - 💼 **LinkedIn** — Profile,jobssearch
>
> ,"Xiaohongshu Twitter"," Facebook  Instagram"."".

Based on the user's choice, run:

```bash
agent-reach install --env=auto --channels=opencli,xiaohongshu   # Example: desktop user chose XHS (OpenCLI-backed)
agent-reach install --env=auto --channels=facebook,instagram    # Example: desktop user chose Meta social channels
agent-reach install --env=auto --channels=all              # User wants everything
```

Supported channel names: `opencli`, `twitter`, `xiaoyuzhou`, `xueqiu`, `xiaohongshu`, `reddit`, `facebook`, `instagram`, `bilibili`, `linkedin`, `all`

### Step 3: Fix what's broken

Run `agent-reach doctor` and check the output.

Try to get as many channels to ✅ as possible. If something failed during install or shows as ❌/⚠️ in doctor, diagnose the problem and try to fix it — but stay within the boundaries above. If a fix requires elevated permissions or system changes, ask the user first.

Only ask the user when you genuinely need their input (credentials, permissions, etc.).

### Step 3: Configure things that need user input

Some channels need credentials only the user can provide. Based on the doctor output, ask for what's missing:

> 🔒 **Security tip:** For platforms that need cookies or browser sessions (Twitter, XiaoHongShu, Reddit, Facebook, Instagram), we recommend using a **dedicated/secondary account** rather than your main account. Cookie/browser-session auth carries two risks:
> 1. **Account ban** — platforms may detect non-browser API calls and restrict or ban the account
> 2. **Credential exposure** — cookies grant full account access; using a secondary account limits the blast radius if credentials are ever compromised

> 🍪 **Cookie / login session:**
>
>  CLI requires Cookie (Twitter,Xueqiu),** Cookie-Editor **,:
> 1. usersbrowserlog in
> 2. install [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) Chrome 
> 3.  → Export → Header String
> 4.  Agent
>
> **users** `agent-reach configure --from-browser chrome` ( Twitter + Xiaohongshu + Xueqiu).OpenCLI (Reddit,Xiaohongshu,Facebook,Instagram) Chrome login session,requires Cookie  Agent.

**Twitter search & posting:**
> "To unlock Twitter search, I need your Twitter cookies. Install the Cookie-Editor Chrome extension, go to x.com/twitter.com, click the extension → Export → Header String, and paste it to me."

```bash
agent-reach configure twitter-cookies "PASTED_STRING"
```

> **proxy(Mainland Chinarequires):**
>
> twitter-cli  rdt-cli  Python,requiresproxyconfigureproxy.
>
> **(Agent)requires:**
> 1. usersproxy:`agent-reach configure proxy http://user:pass@ip:port`
> 2. :`export HTTP_PROXY="..." HTTPS_PROXY="..."`
> 3. Agent Reach ,requiresusers
>
> Ifusers "fetch failed", [troubleshooting.md](troubleshooting.md)

**Reddit (login is mandatory — no zero-config path):**
> Reddit , API .users OpenCLI(browserlog in reddit.com available);/users rdt-cli:

```bash
# PyPI , GitHub (code _RDT_GIT_SOURCE )
pipx install 'git+https://github.com/public-clis/rdt-cli.git@5e4fb3720d5c174e976cd425ccc3b879d52cac66'
rdt login   # browser Cookie;browser doctor  Cookie
```

> Mainland Chinaaccess Reddit requiresproxy; IP proxy( https://webshare.io, $1/):
> ```bash
> agent-reach configure proxy http://user:pass@ip:port
> ```

**XiaoHongShu / Xiaohongshu(,):**

> **(recommended OpenCLI):**
> "Xiaohongshu OpenCLI——browserlogin session,Xiaohongshu,configure."

```bash
agent-reach install --channels opencli
```

> users(Chrome ,):
> 1.  https://chromewebstore.google.com/detail/opencli/ildkmabpimmkaediidaifkhjpohdnifk
> 2. " Chrome"
> 3. run `opencli doctor` ( Extension: connected )
>
> ** / (xiaohongshu-mcp):**
> 1.  https://github.com/xpzouying/xiaohongshu-mcp/releases  binary  `~/.agent-reach/tools/`
> 2. (run 150MB headless browser,)
> 3. usersscan QR codelog in(agent  `get_login_qrcode` Tool)
> 4. :`mcporter config add xiaohongshu http://localhost:18060/mcp`
> 5.  `--timeout 120000`
>
> **users(xhs-cli):**  xhs-cli ( 2026-03 ,recommended).`xhs login` browser Cookie;failed Cookie-Editor :
> ```bash
> agent-reach configure xhs-cookies "key1=val1; key2=val2; ..."
> ```

**Facebook / Instagram( OpenCLI):**
>  OpenCLI:users Chrome login session,save, Meta Graph API ./recommended.

```bash
agent-reach install --channels facebook,instagram
```

> :
> 1.  Chrome install OpenCLI  `opencli doctor`
> 2.  Chrome log in facebook.com / instagram.com
> 3. Agent :
>    ```bash
>    opencli facebook search "query" -f yaml
>    opencli facebook profile zuck -f yaml
>    opencli facebook groups -f yaml
>    opencli instagram search "query" -f yaml     # userssearch
>    opencli instagram profile nasa -f yaml
>    opencli instagram user nasa -f yaml          # usersposts
>    ```
>
> Facebook Groups readuserslog in/,postscomments API.Instagram  search userssearch,postssearch; 429/log in,users Chrome log in.

**Xueqiu / Xueqiu (stock quotes + trendingposts):**
> "Xueqiurequireslog in Cookie. Chrome log in xueqiu.com,run:"

```bash
agent-reach configure --from-browser chrome
```

> Cookie .

**Xiaoyuzhou Podcast / Xiaoyuzhou Podcast (Groq Whisper):**
> "Xiaoyuzhou Podcastinstall,requiresfree Groq API Key."

 Agent Reach install,users Key:

```bash
agent-reach configure groq-key gsk_xxxxx
```

> **get Groq API Key(free,,30 ):**
> 1.  https://console.groq.com
> 2.  Google/GitHub log in()
> 3.  → API Keys → Create API Key
> 4.  Key( `gsk_` ), Agent 
>
> **:**
> usersXiaoyuzhou Agent,Agent :
> ```bash
> bash ~/.agent-reach/tools/xiaoyuzhou/transcribe.sh https://www.xiaoyuzhoufm.com/episode/xxxxx
> ```
>
>  →  → Groq Whisper transcription → Chinese.
>
> **free:**
> -  2 (7200 ), 15 
> - 
> - transcriptionhigh quality(Whisper large-v3),
> - 2 

**LinkedIn ( — linkedin-scraper-mcp):**
> "LinkedIn  Jina Reader read.(Profile details,jobssearch)requires linkedin-scraper-mcp."

```bash
pip install linkedin-scraper-mcp
```

> **log in(requiresbrowser):**
>
> linkedin-scraper-mcp  Chromium browserlog in,requiresbrowser.
>
> - **():** run:
>   ```bash
>   linkedin-scraper-mcp --login --no-headless
>   ```
>   browser,log in LinkedIn .
>
> - **( UI):** requires VNC :
>   ```bash
>   # 1. install VNC()
>   apt install -y tigervnc-standalone-server
>   vncserver :1 -geometry 1280x720
>   
>   # 2.  VNC  IP:5901
>   
>   # 3.  VNC run:
>   export DISPLAY=:1
>   linkedin-scraper-mcp --login --no-headless
>   ```
>    VNC browserlog in.log in session save `~/.linkedin-mcp/profile/`.
>
> **log in MCP :**
> ```bash
> linkedin-scraper-mcp --transport streamable-http --port 8001
> mcporter config add linkedin http://localhost:8001/mcp
> ```
>
>  https://github.com/stickerdaniel/linkedin-mcp-server

### Step 4: Final check

Run `agent-reach doctor` one final time and report the results to your user.

### Step 5: Set up daily monitoring (OpenClaw only)

If you are running inside **OpenClaw**, ask your user:

> "Agent Reach install.?,no.,."

If the user agrees, create a **cron job** (daily, `sessionTarget: "isolated"`, `delivery: "announce"`) with this task:

```
run agent-reach watch .
If"",requiresusers,.
If(❌ ⚠️)(🆕),users,FixesOption.
Ifavailable,users(users Agent :Help me update Agent Reach:https://raw.githubusercontent.com/Panniantong/agent-reach/main/docs/update.md).
```

If the user wants a different agent to handle it, let them choose.

---

## Quick Reference

| Command | What it does |
|---------|-------------|
| `agent-reach install --env=auto` | Install core channels (lightweight, zero-config) |
| `agent-reach install --env=auto --channels=twitter,xiaohongshu` | Install core + optional channels |
| `agent-reach install --env=auto --channels=all` | Install everything |
| `agent-reach install --env=auto --safe` | Safe setup (no auto system changes) |
| `agent-reach install --env=auto --dry-run` | Preview what would be done |
| `agent-reach doctor` | Show channel status |
| `agent-reach watch` | Quick health + update check (for scheduled tasks) |
| `agent-reach check-update` | Check for new versions |
| `agent-reach configure twitter-cookies "..."` | Unlock Twitter search + posting |
| `agent-reach configure proxy URL` | saveproxy(Agent access Reddit/Twitter read HTTP_PROXY/HTTPS_PROXY,) |
| `agent-reach configure groq-key gsk_xxx` | Unlock Xiaoyuzhou podcast transcription |

After installation, use upstream tools directly. See SKILL.md for the full command reference:

| Platform | Upstream Tool | Example |
|----------|--------------|---------|
| Twitter/X | `twitter`( `opencli`) | `twitter search "query" -n 10` |
| YouTube | `yt-dlp` | `yt-dlp --dump-json URL` |
| Bilibili | `bili`(subtitles `opencli`) | `bili search "query" --type video` / `opencli bilibili subtitle BVxxx` |
| Reddit | `opencli`( `rdt`) | `opencli reddit search "query" -f yaml` / `rdt read POST_ID` |
| Facebook | `opencli` | `opencli facebook search "query" -f yaml` |
| Instagram | `opencli` | `opencli instagram user nasa -f yaml` |
| GitHub | `gh` | `gh search repos "query"` |
| Web | `curl` + Jina | `curl -s "https://r.jina.ai/URL"` |
| Exa Search | `mcporter` | `mcporter call 'exa.web_search_exa(...)'` |
| Xiaohongshu | `opencli`( `mcporter`) | `opencli xiaohongshu search "query" -f yaml` |
| Xiaoyuzhou Podcast | `transcribe.sh` | `bash ~/.agent-reach/tools/xiaoyuzhou/transcribe.sh <URL>` |
| LinkedIn | `mcporter` | `mcporter call 'linkedin.get_person_profile(...)'` |
| RSS | `feedparser` | `python3 -c "import feedparser; ..."` |

>  `agent-reach doctor --json`  `active_backend` .
