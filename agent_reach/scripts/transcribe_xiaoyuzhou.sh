#!/bin/bash
# Xiaoyuzhou Podcast
# : bash transcribe.sh [--polish] <Xiaoyuzhou> [file]
# : GROQ_API_KEY (must)
#
# --polish: transcription Groq Llama 3.3 70B Chinese+
#           (Whisper Chinese,)

set -e

POLISH=0
while [ $# -gt 0 ]; do
    case "$1" in
        --polish) POLISH=1; shift ;;
        --) shift; break ;;
        -h|--help)
            echo ": bash transcribe.sh [--polish] <Xiaoyuzhou> [file]"
            exit 0 ;;
        --*)
            echo ": $1" >&2
            exit 1 ;;
        *) break ;;
    esac
done

URL="${1:?: bash transcribe.sh [--polish] <Xiaoyuzhou> [file]}"
OUTPUT="${2:-/tmp/podcast_transcript.txt}"
TMPDIR="/tmp/xiaoyuzhou_$$"

# Try env var first, then agent-reach config.yaml
if [ -z "$GROQ_API_KEY" ]; then
    CONFIG_FILE="$HOME/.agent-reach/config.yaml"
    if [ -f "$CONFIG_FILE" ]; then
        GROQ_API_KEY=$(python3 -c "import yaml; print((yaml.safe_load(open('$CONFIG_FILE')) or {}).get('groq_api_key',''))" 2>/dev/null || true)
    fi
fi
GROQ_API_KEY="${GROQ_API_KEY:? GROQ_API_KEY run agent-reach configure groq-key}"

# Groq API : 25MB per file
MAX_CHUNK_SIZE_MB=20
AUDIO_BITRATE="64k"

cleanup() {
    rm -rf "$TMPDIR"
}
trap cleanup EXIT

mkdir -p "$TMPDIR"

echo "📻 Xiaoyuzhou Podcast"
echo "===================="

# Step 1:  URL 
echo "🔍 ..."
PAGE=$(curl -s "$URL")
AUDIO_URL=$(echo "$PAGE" | perl -ne 'while (/(https:\/\/media\.xyzcdn\.net\/[^"]*\.(?:m4a|mp3))/gi) { print "$1\n" }' | head -1)
TITLE=$(echo "$PAGE" | perl -ne 'if (/"title":"([^"]*)"/) { print "$1\n"; last }' | head -1)

if [ -z "$AUDIO_URL" ]; then
    echo "❌ "
    exit 1
fi

echo "📝 : $TITLE"
echo "🔗 : $AUDIO_URL"

# Step 2: 
echo "⬇️  ..."
EXT="${AUDIO_URL##*.}"
curl -sL -o "$TMPDIR/original.$EXT" "$AUDIO_URL"
FILE_SIZE=$(ls -lh "$TMPDIR/original.$EXT" | awk '{print $5}')
echo "📦 file: $FILE_SIZE"

# Step 3: get
DURATION=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$TMPDIR/original.$EXT" 2>/dev/null | cut -d. -f1)
DURATION_MIN=$((DURATION / 60))
DURATION_SEC=$((DURATION % 60))
echo "⏱️  : ${DURATION_MIN}${DURATION_SEC}"

# Step 4:  MP3
echo "🔄 ..."
ffmpeg -y -i "$TMPDIR/original.$EXT" -b:a "$AUDIO_BITRATE" -ac 1 "$TMPDIR/mono.mp3" 2>/dev/null
MONO_SIZE=$(stat -c%s "$TMPDIR/mono.mp3" 2>/dev/null || stat -f%z "$TMPDIR/mono.mp3")
echo "📦 : $(echo "$MONO_SIZE / 1024 / 1024" | bc)MB"

# Step 5: 
MAX_BYTES=$((MAX_CHUNK_SIZE_MB * 1024 * 1024))

if [ "$MONO_SIZE" -le "$MAX_BYTES" ]; then
    # requires
    cp "$TMPDIR/mono.mp3" "$TMPDIR/chunk_0.mp3"
    NUM_CHUNKS=1
    echo "📎 "
else
    # requires chunk
    NUM_CHUNKS=$(( (MONO_SIZE / MAX_BYTES) + 1 ))
    CHUNK_DURATION=$(( DURATION / NUM_CHUNKS + 10 ))  #  10 
    echo "✂️   $NUM_CHUNKS  ( $((CHUNK_DURATION / 60)) )..."
    
    for i in $(seq 0 $((NUM_CHUNKS - 1))); do
        START=$((i * CHUNK_DURATION))
        ffmpeg -y -i "$TMPDIR/mono.mp3" -ss "$START" -t "$CHUNK_DURATION" -c copy "$TMPDIR/chunk_${i}.mp3" 2>/dev/null
        CHUNK_SIZE=$(ls -lh "$TMPDIR/chunk_${i}.mp3" | awk '{print $5}')
        echo "    $((i+1))/$NUM_CHUNKS: $CHUNK_SIZE"
    done
fi

# Step 6:  Groq Whisper API transcription
echo "🎙️  transcription (Groq Whisper large-v3)..."

for i in $(seq 0 $((NUM_CHUNKS - 1))); do
    echo -n "    $((i+1))/$NUM_CHUNKS... "
    
    RESPONSE=$(curl -s -w "\n%{http_code}" \
        https://api.groq.com/openai/v1/audio/transcriptions \
        -H "Authorization: Bearer $GROQ_API_KEY" \
        -F file="@$TMPDIR/chunk_${i}.mp3" \
        -F model="whisper-large-v3" \
        -F language="zh" \
        -F prompt="Chinese,Chinese(,.?!:;""'')." \
        -F response_format="text")
    
    HTTP_CODE=$(echo "$RESPONSE" | tail -1)
    BODY=$(echo "$RESPONSE" | sed '$d')
    
    if [ "$HTTP_CODE" != "200" ]; then
        echo "❌ API  (HTTP $HTTP_CODE)"
        echo "$BODY"
        
        # If,
        if [ "$HTTP_CODE" = "429" ]; then
            # , 120 
            WAIT_SEC=$(echo "$BODY" | perl -ne 'if (/in (\d+)m/) { print "$1\n"; exit }')
            WAIT_SEC=${WAIT_SEC:-2}
            WAIT_SEC=$((WAIT_SEC * 60 + 30))
            echo "   ⏳ , ${WAIT_SEC} ..."
            sleep "$WAIT_SEC"
            RESPONSE=$(curl -s -w "\n%{http_code}" \
                https://api.groq.com/openai/v1/audio/transcriptions \
                -H "Authorization: Bearer $GROQ_API_KEY" \
                -F file="@$TMPDIR/chunk_${i}.mp3" \
                -F model="whisper-large-v3" \
                -F language="zh" \
                -F prompt="Chinese,Chinese(,.?!:;""'')." \
                -F response_format="text")
            HTTP_CODE=$(echo "$RESPONSE" | tail -1)
            BODY=$(echo "$RESPONSE" | sed '$d')
            
            if [ "$HTTP_CODE" != "200" ]; then
                echo "   ❌ failed"
                exit 1
            fi
        else
            exit 1
        fi
    fi
    
    echo "$BODY" > "$TMPDIR/transcript_${i}.txt"
    CHARS=$(wc -m < "$TMPDIR/transcript_${i}.txt")
    echo "✅ ($CHARS )"
done

# Step 6.5 ():  Llama 3.3 70B +
if [ "$POLISH" = "1" ]; then
    echo "✨ (Llama 3.3 70B +)..."
    for i in $(seq 0 $((NUM_CHUNKS - 1))); do
        echo -n "    $((i+1))/$NUM_CHUNKS... "
        IN_FILE="$TMPDIR/transcript_${i}.txt" \
        OUT_FILE="$TMPDIR/polished_${i}.txt" \
        GROQ_API_KEY="$GROQ_API_KEY" \
        python3 <<'PY'
import json, os, sys, urllib.request, urllib.error

KEY = os.environ["GROQ_API_KEY"]
IN = os.environ["IN_FILE"]
OUT = os.environ["OUT_FILE"]

MODEL = "llama-3.3-70b-versatile"
MAX_DEPTH = 3
PROMPT_TMPL = (
    "Chinese, Whisper Chinese,"
    "no.****:Chinese(,.!?:;),"
    ".\n\n"
    "****:\n"
    "- ,delete,anyEnglish/\n"
    "- ,,\n"
    "- any,,\n"
    "- +\n\n"
    ":\n{}"
)

def call_groq(text):
    body = json.dumps({
        "model": MODEL,
        "temperature": 0.2,
        "max_completion_tokens": 8192,
        "messages": [{"role": "user", "content": PROMPT_TMPL.format(text)}],
    }).encode()
    req = urllib.request.Request(
        "https://api.groq.com/openai/v1/chat/completions",
        data=body,
        headers={
            "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json",
            "User-Agent": "agent-reach-xiaoyuzhou/1.0",
        },
    )
    with urllib.request.urlopen(req, timeout=180) as r:
        resp = json.load(r)
    return (
        resp["choices"][0]["message"]["content"].strip(),
        resp["choices"][0].get("finish_reason"),
    )

def polish(text, depth=0):
    try:
        out, fr = call_groq(text)
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"polish HTTP {e.code}: {e.read().decode(errors='replace')[:200]}\n")
        return text  # fallback to raw
    except Exception as e:
        sys.stderr.write(f"polish error: {e}\n")
        return text
    if fr != "length" or depth >= MAX_DEPTH:
        return out
    # :
    mid = len(text) // 2
    return polish(text[:mid], depth + 1) + polish(text[mid:], depth + 1)

content = open(IN, encoding="utf-8").read().strip()
result = polish(content)
open(OUT, "w", encoding="utf-8").write(result + "\n")
print(f"✅ ({len(result)} )")
PY
    done
fi

# Step 7: 
echo "📄 ..."

{
    echo "# $TITLE"
    echo ""
    echo "Source: $URL"
    echo ": ${DURATION_MIN}${DURATION_SEC}"
    echo "transcription: $(date '+%Y-%m-%d %H:%M')"
    if [ "$POLISH" = "1" ]; then
        echo ": Groq Llama 3.3 70B"
    fi
    echo ""
    echo "---"
    echo ""

    for i in $(seq 0 $((NUM_CHUNKS - 1))); do
        if [ "$POLISH" = "1" ] && [ -f "$TMPDIR/polished_${i}.txt" ]; then
            cat "$TMPDIR/polished_${i}.txt"
        else
            cat "$TMPDIR/transcript_${i}.txt"
        fi
        echo ""
    done
} > "$OUTPUT"

TOTAL_CHARS=$(wc -m < "$OUTPUT")
echo ""
echo "✅ !"
echo "📄 : $OUTPUT"
echo "📊 : $TOTAL_CHARS"
echo "===================="
