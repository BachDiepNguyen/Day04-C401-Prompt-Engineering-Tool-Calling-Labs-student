---
name: url_extract
track: bonus
kind: local_formatter
provider: local
requires_env: []
inputs: [text, max_urls]
outputs: [count, items]
side_effect: false
---

# url_extract

Extracts explicit HTTP/HTTPS URLs from user-provided text and returns normalized URL/domain metadata.
