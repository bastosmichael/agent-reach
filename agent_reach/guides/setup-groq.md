# Groq Whisper configure

## 
 YouTube/Bilibili videonosubtitles, Groq  Whisper API .Groq free.

## Agent 

1. configured:
```bash
agent-reach doctor | grep -i "groq\|whisper"
```

2. Ifusers key,configure:
```python
from agent_reach.config import Config
c = Config()
c.set("groq_api_key", "usersKEY")
```

3. ():
```bash
curl -s https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer usersKEY" \
  -o /dev/null -w "%{http_code}"
```
 200 = available

## requiresusers

users:

> videorequires Groq API Key(free).
>
> :
> 1.  https://console.groq.com
> 2.  Google 
> 3.  "API Keys"
> 4.  "Create API Key"
> 5.  Key,
>
> Groq free,.

## Agent  key 

1. configure:`config.set("groq_api_key", key)`
2.  API available
3. :"✅ !nosubtitlesvideo,."
