---
name: research_metric_compare
track: bonus
kind: local_formatter
provider: local
requires_env: []
inputs: [label_a, value_a, label_b, value_b, metric]
outputs: [difference, percent_change, higher_value]
side_effect: false
---

# research_metric_compare

Compares two numeric research metrics, such as tweet engagement or result counts, and returns difference and percent change.
