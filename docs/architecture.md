# Root Cause architecture

**Data → Knowledge → Memory → Reasoning → Action**

1. **Observe:** ingest incidents, tickets and postmortems locally.
2. **Model:** extract component, symptom, dependency and owner as a failure fingerprint.
3. **Remember:** persist evidence and historical validity in PostgreSQL.
4. **Diagnose:** retrieve evidence and detect recurring patterns across incidents.
5. **Act:** run proposed actions through a policy boundary and append them to a hash chain.

The final Sovereign AI build extends this MVP with pgvector semantic retrieval, local Ollama reasoning, reranking, graph expansion and MCP tools behind a policy gate.
