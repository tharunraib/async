# Root Cause

> **Sovereign causal memory for operations.**

Root Cause learns recurring operational failure patterns from an organisation's own incident history, builds evidence-backed hypotheses, tracks remediation effectiveness, and warns teams before the same failures are repeated.

**ASYNC'26 — Track 1: Sovereign AI** · **Team: Track and Field** · **Ramaiah Institute of Technology**

## Core pipeline

```
Data → Knowledge → Memory → Reasoning → Action
```

## MVP implemented in this repository

- Local incident ingestion and failure fingerprinting
- PostgreSQL + pgvector-ready schema
- Full-text evidence retrieval
- Recurrence clustering
- Pre-flight checks against known failure components
- SHA-256 hash-chained audit events
- Dockerized PostgreSQL environment
- FastAPI service boundary

The final demo architecture described in the project deck extends this foundation with local Ollama models, semantic embeddings, reranking, graph expansion, MCP tools, policy gates, bi-temporal memory and the Next.js console.

## Run locally

### 1. Start PostgreSQL + pgvector

```bash
docker compose up -d postgres
```

### 2. Install backend dependencies

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Start the API

```bash
uvicorn backend.app:app --reload --port 8000
```

Open `http://localhost:8000/docs`.

## API

- `GET /health`
- `POST /api/incidents`
- `GET /api/incidents`
- `POST /api/retrieval/search?query=...`
- `POST /api/clusters/detect`
- `POST /api/preflight`
- `GET /api/audit`

## Documentation

- [Architecture](docs/architecture.md)
- [Demo flow](docs/demo.md)
- [Threat model](docs/threat-model.md)

## Engineering principle

Retrieved content is **evidence, not authority**. Any production action path must be separated behind an explicit policy decision and recorded in an auditable history.

## Status

**Working MVP foundation.** The repository contains runnable ingestion, retrieval, recurrence, pre-flight and audit primitives. Production/demo claims such as measured zero egress, latency, exact recurrence accuracy or completed MCP/policy functionality must be verified against the final integrated prototype before submission.
