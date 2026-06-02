from __future__ import annotations

from typing import Any
from urllib.parse import urlparse


PRIMARY_DOMAINS = {
    "openai.com",
    "anthropic.com",
    "deepmind.google",
    "ai.google",
    "microsoft.com",
    "nvidia.com",
    "arxiv.org",
}

SOCIAL_DOMAINS = {"x.com", "twitter.com", "linkedin.com", "facebook.com"}


def audit_source(url: str = "", source: str = "", claim_type: str = "general") -> dict[str, Any]:
    value = url or source
    domain = urlparse(value).netloc.lower() if value.startswith(("http://", "https://")) else value.lower()
    domain = domain.removeprefix("www.")

    if domain in PRIMARY_DOMAINS or any(domain.endswith("." + item) for item in PRIMARY_DOMAINS):
        rating = "primary"
        guidance = "Good for direct claims about the organization, paper, product, or announcement."
    elif domain in SOCIAL_DOMAINS or any(domain.endswith("." + item) for item in SOCIAL_DOMAINS):
        rating = "social"
        guidance = "Useful as a public signal, but verify factual claims with a primary or reputable news source."
    elif domain:
        rating = "secondary"
        guidance = "Can support context; prefer primary sources for sensitive or precise claims."
    else:
        rating = "unknown"
        guidance = "No source URL/domain was provided."

    return {
        "tool": "audit_source",
        "domain": domain,
        "claim_type": claim_type,
        "rating": rating,
        "guidance": guidance,
    }
