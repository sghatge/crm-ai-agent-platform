from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from crm_ai.agents.executor import execute_tool
from crm_ai.agents.planner import plan_contact_lookup
from crm_ai.audit import audit_event
from crm_ai.policy import Action, authorize_action

app = FastAPI(title="CRM AI Agent Platform", version="0.1.0")


class LookupRequest(BaseModel):
    contact_id: str = Field(min_length=3, max_length=32)
    actor: str = Field(default="local-user", max_length=80)


@app.get("/health")
def health():
    return {"status": "ok", "environment": "development"}


@app.post("/agents/contact-lookup")
def contact_lookup(request: LookupRequest):
    if not authorize_action(Action.READ_CONTACT):
        raise HTTPException(status_code=403, detail="Action not authorized")
    plan = plan_contact_lookup(request.contact_id)
    try:
        result = execute_tool(plan[0]["tool"], plan[0]["arguments"])
    except Exception as exc:
        audit_event("tool_error", request.actor, {"tool": plan[0]["tool"], "error_type": type(exc).__name__})
        raise HTTPException(status_code=400, detail="Tool execution failed") from exc
    audit = audit_event("contact_lookup", request.actor, {"contact_id": request.contact_id, "found": result is not None})
    return {"plan": plan, "result": result, "audit": audit}


@app.post("/policy/check")
def policy_check(action: Action, approved: bool = False):
    return {"action": action, "allowed": authorize_action(action, approved)}
