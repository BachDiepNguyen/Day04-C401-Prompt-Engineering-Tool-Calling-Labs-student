---
name: source_audit
track: bonus
kind: local_knowledge
provider: local
requires_env: []
inputs: [url, source, claim_type]
outputs: [domain, rating, guidance]
side_effect: false
---

# source_audit

Classifies a cited source as primary, social, secondary, or unknown and returns citation guidance.
