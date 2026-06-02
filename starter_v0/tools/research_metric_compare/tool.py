from __future__ import annotations

from typing import Any


def compare_research_metrics(
    label_a: str = "A",
    value_a: float = 0,
    label_b: str = "B",
    value_b: float = 0,
    metric: str = "value",
) -> dict[str, Any]:
    difference = value_b - value_a
    pct_change = None if value_a == 0 else round((difference / value_a) * 100, 2)
    if difference > 0:
        winner = label_b
    elif difference < 0:
        winner = label_a
    else:
        winner = "tie"

    return {
        "tool": "compare_research_metrics",
        "metric": metric,
        "baseline": {"label": label_a, "value": value_a},
        "comparison": {"label": label_b, "value": value_b},
        "difference": difference,
        "percent_change": pct_change,
        "higher_value": winner,
    }
