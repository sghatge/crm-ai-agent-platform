# CRM AI Agent Platform

A runnable, platform-agnostic CRM operations workbench with eight task-specific agent workflows. This starter version works locally without external API credentials. It provides guided inputs, rule-based checks, and structured draft outputs; it does not call a live LLM or CRM API until you configure an integration.

## Quick start (Python 3.10+)

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the local URL Streamlit prints.

## Included agents
- Campaign Manager
- Campaign QA
- Performance Analyst
- CRM Troubleshooter
- Executive Reporting
- Lifecycle & Segmentation
- Workload & Capacity
- Governance & Evidence

## Current capabilities
- Interactive agent selector and task form
- Evidence-first output templates
- Basic deterministic checks for campaign QA, KPI data and workload capacity
- Downloadable Markdown result
- No secrets required for local demo

## Important limitations
This is a functional local prototype, not a production CRM integration. It does not authenticate to a CRM, send messages, deploy campaigns, or call an AI model. The "AI agents" currently use deterministic rules and structured templates. Add a model provider and approved connectors only after reviewing authentication, data privacy, permissions and audit controls.

## Connect an LLM safely
Use a backend service to call your chosen model provider. Store the provider API key in an environment variable or secret manager. Never put keys in Streamlit frontend code, Git, skill files, prompts or downloadable reports. Add authorization, rate limits, input redaction, audit logging and human approval before production writes.

## Suggested roadmap
1. Validate this prototype with synthetic data.
2. Add unit tests and your organization's policy thresholds.
3. Add LLM provider through server-side adapter.
4. Add read-only CRM connector using least-privilege scopes.
5. Add audit log and human-approved write actions.
6. Run a controlled pilot and measure quality, time saved and incidents caught.

## Publish to GitHub
Create a new public repository named `crm-ai-agent-platform` in your GitHub account, then run from this folder:

```bash
git init
git add .
git commit -m "Initial CRM AI Agent Platform"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/crm-ai-agent-platform.git
git push -u origin main
```

Do not commit `.env` files or real customer data.
