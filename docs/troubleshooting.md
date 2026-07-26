# Troubleshooting

## Xueqiu / Xueqiu: API  400

**Symptoms:** `agent-reach doctor` Xueqiu ⚠️, `HTTP Error 400`

**Cause:** Xueqiu API requireslog in Cookie,accessget.

**Solution:**  Chrome log in xueqiu.com,run:

```bash
agent-reach configure --from-browser chrome
```

run `agent-reach doctor`  ✅.Cookie run.

---

## Twitter/X: twitter-cli failed

**Symptoms:** `twitter search` 

**Cause:** twitter-cli requires AUTH_TOKEN  CT0 access Twitter API.Ifrequiresproxyaccess x.com,requiresconfigureproxy.

**Solution:**

### Option 1:proxy

```bash
export HTTP_PROXY="http://user:pass@host:port"
export HTTPS_PROXY="http://user:pass@host:port"
twitter search "test" -n 1
```

### Option 2:proxyTool

proxyTool, twitter-cli proxy:

```bash
# macOS — ClashX / Surge ""
# Linux — proxychains  tun2socks
proxychains twitter search "test" -n 1
```

### Option 3: twitter-cli, Exa search

twitter-cli available, Exa search Twitter :

```bash
mcporter call 'exa.web_search_exa(query: "site:x.com search", numResults: 5)'
```

### Option 4:authentication

```bash
twitter check
```

> If "Missing credentials",requires AUTH_TOKEN  CT0 .
>
> **Fallback:** Ifinstall bird CLI(`npm install -g @steipete/bird`),.Agent Reach installTool.
