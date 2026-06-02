from __future__ import annotations

from typing import Any


GLOSSARY = {
    "prompt engineering": {
        "term": "prompt engineering",
        "definition": "The practice of writing instructions, context, constraints, and examples so a model behaves reliably.",
        "related": ["system prompt", "few-shot", "tool schema"],
    },
    "tool calling": {
        "term": "tool calling",
        "definition": "A control-flow pattern where a model emits a structured function call and the application executes the function.",
        "related": ["tool schema", "agent loop", "guardrail"],
    },
    "system prompt": {
        "term": "system prompt",
        "definition": "The highest-priority instruction layer that defines the agent role, rules, boundaries, and output contract.",
        "related": ["policy", "boundary", "output contract"],
    },
    "prompt injection": {
        "term": "prompt injection",
        "definition": "An attempt to override higher-priority instructions through user input or untrusted retrieved content.",
        "related": ["guardrail", "instruction hierarchy", "least privilege"],
    },
    "parallel tool calling": {
        "term": "parallel tool calling",
        "definition": "Calling independent tools in the same round when their inputs do not depend on each other.",
        "related": ["merge", "tool result", "latency"],
    },
}


def lookup_glossary(term: str = "", top_k: int = 3) -> dict[str, Any]:
    query = (term or "").strip().lower()
    matches = []
    for key, item in GLOSSARY.items():
        if query in key or key in query or any(query in rel for rel in item["related"]):
            matches.append(item)
    if not matches and query:
        for key, item in GLOSSARY.items():
            score = sum(1 for token in query.split() if token in key)
            if score:
                matches.append(item)
    return {
        "tool": "lookup_glossary",
        "query": term,
        "items": matches[:top_k],
    }
