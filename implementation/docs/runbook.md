# Development runbook

1. Create a virtual environment and install `.[dev]`.
2. Start API: `uvicorn crm_ai.api:app --reload`.
3. Check `/health` and `/docs`.
4. Run `pytest -q`.
5. Use only synthetic data until a reviewed sandbox integration is approved.
6. Before adding a write tool: define schema, authorization, approval, idempotency, audit event, tests, and rollback.
7. Never commit secrets.
