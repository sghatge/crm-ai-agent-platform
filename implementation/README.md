# CRM AI Agent Platform — Phase 1 scaffold

This directory contains the governed CRM agent platform implementation baseline. It is additive: the repository's existing root files are preserved.

## Quick start

```bash
cd implementation
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\Activate.ps1
pip install -e ".[dev]"
uvicorn crm_ai.api:app --reload
```

Open `http://127.0.0.1:8000/docs` and check `GET /health`.

## Current capability
- Read-only synthetic CRM contact lookup.
- Allow-listed tool execution.
- Basic policy gate that fails closed for send/update/delete actions.
- Structured audit event response (in-memory demo only).
- API tests.

## Safety boundary
No live CRM credentials, real customer data, campaign dispatch, or destructive actions. Authentication, durable audit storage, tenant isolation, and a real approval service are required before sandbox or production integration.