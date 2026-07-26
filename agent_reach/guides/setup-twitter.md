# Twitter configure(twitter-cli)

Twitter  Jina Reader freeavailable,configure.

requires twitter-cli(@public-clis/twitter-cli):

- search(`twitter search`)
- read(`twitter tweet`,`twitter thread`)
- users(`twitter timeline`)
- (`twitter article`)

twitter-cli freeTool(pipx install),requires Twitter  cookie.

## configure

1.  twitter-cli install:

```bash
which twitter && echo "installed" || echo "not installed"
```

2. install twitter-cli:

```bash
pipx install twitter-cli
```

3. configure:

```bash
twitter search "test" -n 1
```

## get Cookie(Cookie-Editor ,recommended)

1. install [Cookie-Editor](https://cookie-editor.com/) browser
2. log in x.com
3.  Cookie-Editor  → Export → 
4. runconfigure:

```bash
agent-reach configure twitter-cookies " cookie JSON"
```

 `auth_token`  `ct0`,.

##  Cookie

If `auth_token`  `ct0`:

1. install twitter-cli(If):`pipx install twitter-cli`

2. :

```bash
export AUTH_TOKEN="auth_token"
export CT0="ct0"
```

3. :

```bash
twitter search "test" -n 1
```

## proxyconfigure

> twitter-cli proxy:

```bash
export HTTP_PROXY="http://user:pass@host:port"
export HTTPS_PROXY="http://user:pass@host:port"
twitter search "test" -n 1
```

proxyTool:

```bash
proxychains twitter search "test" -n 1
```

## Fallback:bird CLI

Ifinstall [bird CLI](https://www.npmjs.com/package/@steipete/bird)(`npm install -g @steipete/bird`),.Agent Reach install bird.,twitter-cli recommendedOption.
