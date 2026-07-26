# video/

YouTube,Bilibili,Xiaoyuzhou Podcastsubtitlestranscription.

## YouTube (yt-dlp)

### getvideodata

```bash
yt-dlp --dump-json "URL"
```

### subtitles

```bash
# subtitles (video)
yt-dlp --write-sub --write-auto-sub --sub-lang "zh-Hans,zh,en" --skip-download -o "/tmp/%(id)s" "URL"

# read .vtt file
cat /tmp/VIDEO_ID.*.vtt
```

### getcomments

```bash
# comments(best-effort,)
yt-dlp --write-comments --skip-download --write-info-json \
  --extractor-args "youtube:max_comments=20" \
  -o "/tmp/%(id)s" "URL"
# comments .info.json  comments 
```

### searchvideo

```bash
yt-dlp --dump-json "ytsearch5:query"
```

> **subtitles**: subtitles;subtitles,.
> **comments**: `--write-comments` web page( YouTube Data API),comments.

### subtitles:Whisper 

```bash
# videonosubtitles: Whisper (Groq free key )
agent-reach transcribe "https://www.youtube.com/watch?v=VIDEO_ID"
agent-reach transcribe ./local_audio.mp3 -o /tmp/transcript.txt
```

> `agent-reach transcribe`  http(s) URL file. `ytsearch5:` search, yt-dlp video URL,.
> requiresconfigure key:`agent-reach configure groq-key gsk_xxx`(free,console.groq.com)
>  `agent-reach configure openai-key sk-xxx`. auto :groq failed openai.

## Bilibili / Bilibili(bili-cli ,OpenCLI subtitles)

> ⚠️ ** yt-dlp  Bilibili**:Bilibili 412  yt-dlp(,/proxy/ Cookie ).yt-dlp  YouTube.

### videodetails/search/trending/ (bili-cli,no login required)

```bash
# videodetails(/UP//data/subtitlesavailable)
bili video BVxxx

# searchvideo
bili search "query" --type video -n 5

# trendingvideo / 
bili hot -n 10
bili rank -n 10

#  ASR-ready WAV(subtitles agent-reach transcribe )
bili audio BVxxx
```

### subtitles (OpenCLI,requires Chrome)

```bash
# subtitles
opencli bilibili subtitle BVxxx

# OpenCLI search/videodata()
opencli bilibili search "query" -f yaml
opencli bilibili video BVxxx -f yaml
```

### configure:search API 

```bash
UA="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
curl -s -c /tmp/bili_ck.txt -o /dev/null -A "$UA" "https://www.bilibili.com/"
curl -s -b /tmp/bili_ck.txt -A "$UA" -e "https://www.bilibili.com/" \
  "https://api.bilibili.com/x/web-interface/search/all/v2?keyword=QUERY&page=1"
```

> **install bili-cli**: `pipx install bilibili-cli`( 2026-03 ;Scenariono login required,`bili login` scan QR code/).

## Xiaoyuzhou Podcast / Xiaoyuzhou Podcast

### transcription( --polish )

```bash
#  Markdown file /tmp/.--polish  Llama 3.3 70B Chinese+
~/.agent-reach/tools/xiaoyuzhou/transcribe.sh --polish "https://www.xiaoyuzhoufm.com/episode/EPISODE_ID"
```

>  prompt  Whisper Chinese;, `--polish`  Groq free Llama 3.3 70B +(9  ~7 ). LLM ,.

### 

1. **ffmpeg**: `brew install ffmpeg`
2. **Groq API Key** (free): https://console.groq.com/keys
3. **configure Key**: `agent-reach configure groq-key YOUR_KEY`
4. **run**: `agent-reach install --env=auto` installTool

### status

```bash
agent-reach doctor
```

>  Markdown filesave `/tmp/`.

## Selection guide

| Scenario | recommendedTool |
|-----|---------|
| YouTube subtitles | yt-dlp |
| Bilibilivideodetails/search | bili-cli |
| Bilibilisubtitles | opencli bilibili subtitle |
| transcription | Xiaoyuzhou transcribe.sh |
| subtitlesvideo | agent-reach transcribe(Bilibili `bili audio`) |
