# Root Cause

> **Sovereign causal memory for operations.**

Root Cause is a local-first incident-intelligence system that learns recurring operational failure patterns from an organisation's own incident history, builds evidence-backed causal hypotheses, tracks remediation effectiveness, and warns teams before the same failures are repeated.

**ASYNC'26 — Track 1: Sovereign AI**  
**Team:** Track and Field  
**Institute:** Ramaiah Institute of Technology

## The core idea

Traditional incident workflows restore service, but the underlying cause can survive the fix. Root Cause treats the **failure pattern**, not the document, as the unit of intelligence.

```
Data → Knowledge → Memory → Reasoning → Action
```

## What the MVP implements

- Local PDF/Markdown/text ingestion
- Failure fingerprint extraction
- PostgreSQL + pgvector persistence
- Full-text + vector retrieval
- Bi-temporal incident facts
- Recurrence clustering using multiple signals
- Evidence-backed causal hypotheses
- Deterministic failure-debt scoring
- Pre-flight change checks
- Policy-gated actions
- SHA-256 hash-chained audit records
- Local Ollama inference
- FastAPI service boundary
- Next.js console boundary

## Repository structure

```
backend/       FastAPI + domain services
frontend/      Next.js console
database/      PostgreSQL schema
docs/          Architecture, design and threat model
tests/         Automated tests
scripts/       Repeatable local/demo utilities
```

## Quick start

### Requirements

- Python 3.11+
- Node.js 20+
- Docker + Docker Compose
- PostgreSQL 16 with pgvector
- Ollama (optional for model-backed extraction/reasoning)

### Environment

```bash
cp .env.example .env
```

### Start PostgreSQL

```bash
docker compose up -d postgres
```

### Backend

```bash
cd backend
python -m venv .venv
# Windows:
.venv\\Scripts\\activate
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### API

Open `http://localhost:8000/docs`.

Key endpoints:

- `POST /api/incidents` — ingest an incident
- `GET /api/incidents` — list incidents
- `POST /api/retrieval/search` — retrieve evidence
- `POST /api/clusters/detect` — detect recurrence clusters
- `POST /api/preflight` — check a proposed change
- `GET /api/audit` — inspect the audit chain
- `GET /health` — service health

## Architecture

See [docs/architecture.md](docs/architecture.md).

## Security model

Retrieved content is treated as **evidence, not authority**. Actions require a policy decision and are recorded in the audit chain. The intended deployment keeps incident data and inference on organisation-controlled hardware.

## Demo

See [docs/demo.md](docs/demo.md) for the controlled ASYNC'26 scenario.

## Important status note

This repository is the implementation base for the Root Cause MVP. Claims in the pitch deck such as measured egress, latency, dataset size, or specific demo outcomes should only be reported as achieved after they have been run and measured on the final prototype.

## Team

- Anshuman Vijayvargiya
- Tharun Rai B
- Tobie Manoj
- Vatsal Kalra
