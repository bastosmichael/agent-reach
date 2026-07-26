# Social media & communities

Xiaohongshu,Twitter/X,Bilibili,V2EX,Reddit,Facebook,Instagram.

## Xiaohongshu / XiaoHongShu()

Xiaohongshu,** `agent-reach doctor --json`  xiaohongshu  `active_backend` **,.

###  A:OpenCLI(,reuse browserlogin session)

```bash
# search
opencli xiaohongshu search "query" -f yaml

# +data(search URL, xsec_token)
opencli xiaohongshu note "NOTE_URL" -f yaml

# comments()
opencli xiaohongshu comments NOTE_ID -f yaml

# recommended feed
opencli xiaohongshu feed -f yaml

# users
opencli xiaohongshu user USER_ID -f yaml
```

>  Chrome  OpenCLI . AUTH_REQUIRED browserlog inXiaohongshu,users Chrome log in.

###  B:xiaohongshu-mcp(Scenario)

```bash
# not logged in:status,users
mcporter call 'xiaohongshu.check_login_status()' --timeout 120000
mcporter call 'xiaohongshu.get_login_qrcode()' --timeout 120000

# search
mcporter call 'xiaohongshu.search_feeds(keyword: "query")' --timeout 120000

# details+comments(feed_id  xsec_token search)
mcporter call 'xiaohongshu.get_feed_detail(feed_id: "...", xsec_token: "...")' --timeout 120000
```

>  150MB headless browser, `--timeout 120000`.not logged in search , check_login_status.

###  C:xhs-cli(, 2026-03 )

```bash
xhs search "query"          # search
xhs read NOTE_ID_OR_URL     # (mustsearch URL/ID, note_id)
xhs comments NOTE_ID_OR_URL # comments
xhs hot                     # trending
xhs feed                    # recommended
```

> :`xhs user` / `xhs user-posts` / `xhs favorites`  API error().users A/B.

### 

> **xsec_token **: Xiaohongshu xsec_token ,** note_id **.:search/feed , URL/ID ..
>
> ****: (search,comments),. 2-3 .
>
> **(/comments/)**: .xhs-cli v0.6.x  406.

## Twitter/X (twitter-cli)

### 

```bash
# ()
twitter feed -n 20

# read(replies)
twitter tweet URL_OR_ID

# read / X Article
twitter article URL_OR_ID

# users
twitter user-posts @username -n 20

# users
twitter user @username
```

### 

```bash
# search(Twitter  GraphQL , 404)
twitter search "query" -n 10

# likes(2024 ,)
twitter likes
```

### search failed(,)

1. (failed):`twitter search "query" -n 10`
2. :`pipx upgrade twitter-cli && twitter search "query" -n 10`
3.  OpenCLI (,reuse browserlogin session):`opencli twitter search "query" -f yaml`
4.  `twitter feed` / `twitter user-posts @somebody` 

### 

> **install**: `pipx install twitter-cli`( v0.8.5+)
>
> **authentication**: recommended Cookie-Editor  `TWITTER_AUTH_TOKEN` + `TWITTER_CT0`. SSH/Docker/available.
>
> **IP **:  VPS/data IP , followers/following,.proxy.
>
> **OpenCLI **:  OpenCLI ,`opencli twitter search/article/user-posts -f yaml` available(browserlogin session, cookie ).
>
> **format**:  `--yaml`  `--json` , AI agent .

## Bilibili / Bilibili

> ⚠️ ** yt-dlp  Bilibili**( 412 ,). bili-cli / OpenCLI.

```bash
# search / trending / videodetails(bili-cli,no login required)
bili search "query" --type video -n 5
bili hot -n 10
bili video BVxxx

# subtitles(OpenCLI, Chrome)
opencli bilibili subtitle BVxxx
```

> (,API ) [references/video.md](video.md).

## V2EX ( API)

authentication, API.

### trendingtopics

```bash
curl -s "https://www.v2ex.com/api/topics/hot.json" -H "User-Agent: agent-reach/1.0"
```

### nodestopics

```bash
# node_name : python, tech, jobs, qna, programmers
curl -s "https://www.v2ex.com/api/topics/show.json?node_name=python&page=1" -H "User-Agent: agent-reach/1.0"
```

### topicsdetails

```bash
# topic_id  URL get, https://www.v2ex.com/t/1234567
curl -s "https://www.v2ex.com/api/topics/show.json?id=TOPIC_ID" -H "User-Agent: agent-reach/1.0"
```

### topicsreplies

```bash
curl -s "https://www.v2ex.com/api/replies/show.json?topic_id=TOPIC_ID&page=1" -H "User-Agent: agent-reach/1.0"
```

### user information

```bash
curl -s "https://www.v2ex.com/api/members/show.json?username=USERNAME" -H "User-Agent: agent-reach/1.0"
```

### Python 

```python
from agent_reach.channels.v2ex import V2EXChannel

ch = V2EXChannel()

# gettrendingposts
topics = ch.get_hot_topics(limit=10)
for t in topics:
    print(f"[{t['node_title']}] {t['title']} ({t['replies']} replies)")

# getnodesposts
node_topics = ch.get_node_topics("python", limit=5)

# getpostsdetails + replies
topic = ch.get_topic(1234567)
print(topic["title"], "—", topic["author"])

# getuser information
user = ch.get_user("Livid")
```

> **nodes**: https://www.v2ex.com/planes

## Reddit(,mustlogin session)

**Reddit noconfigure**: `.json` (403), API  2025-11 .login session, `agent-reach doctor --json`  reddit  `active_backend`.Mainland Chinaaccessproxy.

###  A:OpenCLI(,reuse browserlogin session)

```bash
# searchposts
opencli reddit search "query" -f yaml

# posts + comments
opencli reddit read POST_ID -f yaml

#  subreddit / trending / Popular
opencli reddit subreddit LocalLLaMA -f yaml
opencli reddit hot -f yaml
opencli reddit popular -f yaml

# subreddit (,)
opencli reddit subreddit-info LocalLLaMA -f yaml
```

>  Chrome browserlog in reddit.com.

###  B:rdt-cli(/, 2026-03 )

```bash
rdt search "query" --limit 10   # searchposts
rdt read POST_ID                # posts + comments
rdt sub python --limit 20       #  subreddit
rdt popular --limit 10          # trending
rdt all --limit 10              #  /r/all
```

> **install**: `pipx install 'git+https://github.com/public-clis/rdt-cli.git'`(PyPI , GitHub  v0.4.2+). `rdt login` search(browser Cookie, doctor ).
>  `--yaml` , AI agent .

### : API + PRAW(users)

2025-11  Reddit script app( client_id/client_secret)users PRAW  API(100 QPM free).,**recommendedusers**.

## Facebook(OpenCLI,mustlogin session)

Facebook  OpenCLI,users Chrome  facebook.com login session. `agent-reach doctor --json`  facebook  `active_backend`, `OpenCLI`.recommended Jina/Exa/Graph API .

```bash
# searchusers /  / posts
opencli facebook search "query" -f yaml

# users
opencli facebook profile zuck -f yaml

#  News Feed
opencli facebook feed --limit 10 -f yaml

# /
opencli facebook groups --limit 20 -f yaml
```

>  Chrome  OpenCLI ,log in facebook.com.Facebook Groups read/,postscomments API.

## Instagram(OpenCLI,mustlogin session)

Instagram  OpenCLI,users Chrome  instagram.com login session. `agent-reach doctor --json`  instagram  `active_backend`, `OpenCLI`. instaloader; cookies/401/429 .

```bash
# searchusers(postssearch)
opencli instagram search "query" -f yaml

# users Profile
opencli instagram profile nasa -f yaml

# usersposts
opencli instagram user nasa --limit 12 -f yaml

# Explore / Discover
opencli instagram explore --limit 20 -f yaml

# 
opencli instagram saved --limit 20 -f yaml
```

>  Chrome  OpenCLI ,log in instagram.com.`instagram search` userssearch;postsrequires username, `instagram user USERNAME`. 429 / login required,users Chrome log in.
