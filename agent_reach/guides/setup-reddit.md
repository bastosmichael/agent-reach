# Reddit configure

## 

Reddit browseraccess(data ISP proxy IP),JSON API  403.

Agent Reach  **rdt-cli**  Reddit search:
- **search**:`rdt search ""`
- **posts+comments**:`rdt read POST_ID`

free,proxy, API Key.requireslog inauthentication(`rdt login`,browser Cookie).

## Agent 

1.  rdt-cli available:
```bash
which rdt && echo "installed" || echo "not installed"
```

2. Ifnot installed,install(PyPI , GitHub install):
```bash
pipx install 'git+https://github.com/public-clis/rdt-cli.git'
```

install:
```bash
agent-reach install --env=auto --channels=reddit
```

## 

search Reddit :
```bash
rdt search "python best practices" -n 5
```

postscomments:
```bash
rdt read POST_ID
```

## requiresusers

.rdt-cli  `agent-reach install --env=auto` install.

## Fallback:Exa search

Ifconfigure Exa( mcporter), Exa search Reddit :

```bash
mcporter call 'exa.web_search_exa(query: "python best practices", numResults: 5, includeDomains: ["reddit.com"])'
```

rdt-cli recommendedOption,configure.
