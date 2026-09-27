# Threat model

### Assets
Incident reports, infrastructure details, customer-impact information, remediation history and action logs.

### Threats
- Sensitive data egress
- Prompt injection in retrieved documents
- Unauthorised automated actions
- Audit tampering
- Overconfident causal claims

### Controls
- Local inference/retrieval boundary
- Evidence citations
- Policy gate before actions
- SHA-256 hash-chained audit records
- Explicit remediation outcomes
- Quarantine path for untrusted input
