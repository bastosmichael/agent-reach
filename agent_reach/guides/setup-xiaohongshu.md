# Xiaohongshuconfigure

## 
readsearchXiaohongshu. [xhs-cli](https://github.com/jackwener/xiaohongshu-cli)(⭐1.5K,pipx install).

## 
- Python 3.10+(pipx install)
- browserlog in xiaohongshu.com( Cookie)

## Agent 

### 1. install xhs-cli
```bash
pipx install xiaohongshu-cli
```

### 2. log in(browser Cookie)
```bash
xhs login
```

> browser Cookie.Iffailed,().

### 3. 
```bash
agent-reach doctor
```

Xiaohongshu ✅.

## requiresusers

If `xhs login` failed,requires cookies:

> **recommended:Cookie-Editor browser()**
>
> 1.  Chrome install [Cookie-Editor](https://chromewebstore.google.com/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm) 
> 2. browserlog in xiaohongshu.com
> 3.  Cookie-Editor  → Export → Header String
> 4.  Agent,run:`agent-reach configure xhs-cookies "cookie"`
>
> ****: QR scan QR codelog in,Cookie-Editor .

## 

search:
```bash
xhs search ""
```

details:
```bash
xhs read NOTE_ID
```

comments:
```bash
xhs comments NOTE_ID
```

## 

**Q: Cookie ?**
A: run `xhs login`  Cookie-Editor .

**Q: Xiaohongshu IP ?**
A: recommendedproxy:`export HTTP_PROXY="http://user:pass@ip:port"`.

**Q: xhs-cli ?**
A:  Python 3.10+  pipx install.run `pipx install xiaohongshu-cli` .

## Option:Docker MCP

If [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) Docker Option,:

```bash
docker run -d \
  --name xiaohongshu-mcp \
  -p 18060:18060 \
  xpzouying/xiaohongshu-mcp

mcporter config add xiaohongshu http://localhost:18060/mcp
```

xhs-cli recommendedOption,requires Docker,install.
