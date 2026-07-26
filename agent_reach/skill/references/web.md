# Web reading

General web pages,RSS.

## General web pages (Jina Reader)

```bash
# readany web page
curl -s "https://r.jina.ai/URL"

# 
curl -s "https://r.jina.ai/https://example.com/article"
```

**Scenario**: web page Jina Reader read.

## Web Reader (MCP)

```bash
# readweb page (Markdown format)
mcporter call 'web-reader.webReader(url: "https://example.com")'

# images
mcporter call 'web-reader.webReader(url: "https://example.com", retain_images: true)'

# plain textformat
mcporter call 'web-reader.webReader(url: "https://example.com", return_format: "text")'
```

**Scenario**: requiresformat.

## RSS (feedparser)

```python
python3 -c "
import feedparser
for e in feedparser.parse('FEED_URL').entries[:5]:
    print(f'{e.title} — {e.link}')
"
```

**Scenario**: blogs,news feeds, RSS feed.

## Selection guide

| Scenario | recommendedTool |
|-----|---------|
| General web pages | Jina Reader (`curl r.jina.ai`) |
| requiresimages/format | web-reader MCP |
| RSS  | feedparser |
