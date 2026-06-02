from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlparse


URL_RE = re.compile(r"https?://[^\s<>)\]\"']+", re.IGNORECASE)


def extract_urls(text: str = "", max_urls: int = 20) -> dict[str, Any]:
    urls: list[str] = []
    for match in URL_RE.findall(text or ""):
        cleaned = match.rstrip(".,;:!?")
        if cleaned not in urls:
            urls.append(cleaned)
        if len(urls) >= max_urls:
            break

    items = []
    for url in urls:
        parsed = urlparse(url)
        items.append({
            "url": url,
            "domain": parsed.netloc.lower(),
            "scheme": parsed.scheme,
        })

    return {
        "tool": "extract_urls",
        "count": len(items),
        "items": items,
    }
