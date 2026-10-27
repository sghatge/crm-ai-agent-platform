import json
from datetime import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="CRM AI Agent Platform", page_icon="🧭", layout="wide")

AGENTS = {
    "Campaign Manager": "Plan, track, and unblock campaigns.",
    "Campaign QA": "Check campaign readiness and launch risks.",
    "Performance Analyst": "Calculate KPIs and identify patterns.",
    "CRM Troubleshooter": "Structure incident diagnosis and safe next steps.",
    "Executive Reporting": "Turn evidence into leadership-ready updates.",
    "Lifecycle & Segmentation": "Review journeys, audience logic and suppression.",
    "Workload & Capacity": "Model demand, capacity and potential savings.",
    "Governance & Evidence": "Audit claims, sources, privacy and approval gaps.",
}

def evidence(label, value):
    return {"label": label, "value": value.strip() if isinstance(value, str) else value}

def campaign_qa(data):
    checks = []
    def add(name, ok, detail, severity="HIGH"):
        checks.append({"Check": name, "Status": "PASS" if ok else "NOT VERIFIED / REVIEW", "Severity": severity if not ok else "—", "Evidence / next step": detail})
    add("Campaign ID supplied", bool(data["campaign_id"]), "Provided ID: " + (data["campaign_id"] or "Missing"))
    add("Consent evidence", bool(data["consent"]), "Evidence supplied: " + (data["consent"] or "No consent evidence supplied"))
    add("Audience and exclusions", bool(data["audience"]), "Audience definition: " + (data["audience"] or "Missing audience definition"))
    add("Proof / content reviewed", bool(data["proof"]), "Proof reference: " + (data["proof"] or "No proof reference supplied"), "MEDIUM")
    add("Approval evidence", bool(data["approval"]), "Approval reference: " + (data["approval"] or "No approval evidence supplied"))
    add("Schedule supplied", bool(data["schedule"]), "Schedule: " + (data["schedule"] or "Missing schedule"), "MEDIUM")
    blocker = any(c["Status"] != "PASS" and c["Severity"] == "HIGH" for c in checks)
    verdict = "NO-GO / INSUFFICIENT EVIDENCE" if blocker else "GO WITH CONDITIONS — HUMAN REVIEW REQUIRED"
    return verdict, pd.DataFrame(checks), "This checklist is a preliminary evidence check, not a substitute for platform validation or authorized human approval."

def performance(data):
    rows = []
    sent = data.get("sent", 0)
    delivered = data.get("delivered", 0)
    opens = data.get("opens", 0)
    clicks = data.get("clicks", 0)
    conversions = data.get("conversions", 0)
    def rate(n, d):
        return f"{(n/d*100):.2f}%" if d and n >= 0 else "Not available"
    rows.extend([
        {"Metric":"Delivery rate","Value":rate(delivered,sent),"Basis":f"{delivered:,} delivered / {sent:,} sent"},
        {"Metric":"Unique open rate (approx.)","Value":rate(opens,delivered),"Basis":f"{opens:,} opens / {delivered:,} delivered; confirm source definition"},
        {"Metric":"CTR (approx.)","Value":rate(clicks,delivered),"Basis":f"{clicks:,} clicks / {delivered:,} delivered; confirm unique vs total clicks"},
        {"Metric":"Conversion rate (approx.)","Value":rate(conversions,delivered),"Basis":f"{conversions:,} conversions / {delivered:,} delivered; attribution window not provided"},
    ])
    notes = []
    if sent <= 0: notes.append("Sent must be greater than zero for meaningful rates.")
    if delivered > sent: notes.append("Delivered exceeds sent; validate source definitions or data quality.")
    if opens > delivered: notes.append("Opens exceed delivered; verify whether opens are total rather than unique.")
    if clicks > delivered: notes.append("Clicks exceed delivered; verify total/unique definitions.")
    if not notes: notes.append("Rates are descriptive only. Confirm source definitions, time window, attribution and deduplication before decisions.")
    return pd.DataFrame(rows), notes

def workload(data):
    hours = float(data["hours"])
    capacity = float(data["capacity"])
    util = (hours / capacity * 100) if capacity > 0 else None
    overload = max(0.0, hours-capacity)
    rows = [
        {"Metric":"Demand hours","Value":f"{hours:.1f}"},
        {"Metric":"Available capacity hours","Value":f"{capacity:.1f}"},
        {"Metric":"Utilization","Value":f"{util:.1f}%" if util is not None else "Not available"},
        {"Metric":"Overload hours","Value":f"{overload:.1f}"},
    ]
    return pd.DataFrame(rows)

def generic_output(agent, task, context):
    return f"""# {agent} — Draft Output

## Request
{task}

## Evidence provided
{context if context else "No supporting evidence supplied."}

## Initial assessment
- **Status:** NOT VERIFIED — this prototype cannot verify external systems or evidence not included above.
- **Recommendation:** Use the supplied context to identify the next check; attach source artifacts before making operational decisions.
- **Human review:** Required before sending messages, changing audience rules, updating production systems, or launching campaigns.

## Missing information / limitations
- Exact source files, platform records, definitions and approval evidence may be required.
- Any inference must be labelled as a hypothesis.
- No external CRM or model-provider call was made by this local prototype.
"""

st.title("CRM AI Agent Platform")
st.caption("A local, evidence-first workbench for CRM and marketing operations.")
st.warning("Prototype mode: no live CRM connection, no external AI model call, and no outbound actions. Use synthetic or sanitized data.")

with st.sidebar:
    st.header("Agent")
    agent = st.selectbox("Choose an agent", list(AGENTS.keys()))
    st.write(AGENTS[agent])
    st.divider()
    st.markdown("**Operating rules**")
    st.markdown("- Evidence before conclusions\n- Missing evidence = not verified\n- Human approval for production actions\n- Never paste secrets or unnecessary personal data")

left, right = st.columns([1.1, 0.9], gap="large")
with left:
    st.subheader("Task intake")
    task = st.text_input("What do you need the agent to do?", placeholder="e.g. Review campaign readiness for next week's launch")
    context = st.text_area("Paste sanitized evidence or context", height=180, placeholder="Campaign brief, aggregate metrics, sanitized logs, ticket notes...")
    with st.form("agent_form"):
        st.markdown("#### Optional structured inputs")
        if agent == "Campaign QA":
            campaign_id = st.text_input("Campaign ID")
            consent = st.text_input("Consent / opt-in evidence reference")
            audience = st.text_input("Audience and exclusion definition")
            proof = st.text_input("Proof / content reference")
            approval = st.text_input("Approval evidence reference")
            schedule = st.text_input("Planned schedule and time zone")
            submitted = st.form_submit_button("Run QA checks", type="primary")
        elif agent == "Performance Analyst":
            sent = st.number_input("Sent", min_value=0, value=10000, step=100)
            delivered = st.number_input("Delivered", min_value=0, value=9800, step=100)
            opens = st.number_input("Opens (specify unique or total in context)", min_value=0, value=4500, step=100)
            clicks = st.number_input("Clicks (specify unique or total in context)", min_value=0, value=350, step=10)
            conversions = st.number_input("Conversions", min_value=0, value=45, step=1)
            submitted = st.form_submit_button("Calculate KPIs", type="primary")
        elif agent == "Workload & Capacity":
            hours = st.number_input("Demand hours for period", min_value=0.0, value=240.0, step=10.0)
            capacity = st.number_input("Available capacity hours", min_value=0.0, value=220.0, step=10.0)
            submitted = st.form_submit_button("Calculate capacity", type="primary")
        else:
            submitted = st.form_submit_button("Generate structured draft", type="primary")

with right:
    st.subheader("Agent output")
    if submitted:
        st.session_state["last_run"] = {
            "agent": agent,
            "task": task or "Task not specified",
            "context": context,
            "time": datetime.now().isoformat(timespec="seconds")
        }
        if agent == "Campaign QA":
            verdict, df, note = campaign_qa({
                "campaign_id": campaign_id, "consent": consent, "audience": audience,
                "proof": proof, "approval": approval, "schedule": schedule
            })
            st.session_state["qa"] = {"verdict": verdict, "table": df, "note": note}
            st.session_state.pop("perf", None)
            st.session_state.pop("workload", None)
        elif agent == "Performance Analyst":
            df, notes = performance({"sent":sent,"delivered":delivered,"opens":opens,"clicks":clicks,"conversions":conversions})
            st.session_state["perf"] = {"table":df,"notes":notes}
            st.session_state.pop("qa", None)
            st.session_state.pop("workload", None)
        elif agent == "Workload & Capacity":
            df = workload({"hours":hours,"capacity":capacity})
            st.session_state["workload"] = df
            st.session_state.pop("qa", None)
            st.session_state.pop("perf", None)
        else:
            st.session_state["generic"] = generic_output(agent, task or "Task not specified", context)
            st.session_state.pop("qa", None)
            st.session_state.pop("perf", None)
            st.session_state.pop("workload", None)

    if "qa" in st.session_state:
        result = st.session_state["qa"]
        st.markdown(f"### Verdict: {result['verdict']}")
        st.dataframe(result["table"], use_container_width=True, hide_index=True)
        st.info(result["note"])
        output_text = f"Verdict: {result['verdict']}\n\n{result['table'].to_markdown(index=False)}\n\n{result['note']}"
    elif "perf" in st.session_state:
        result = st.session_state["perf"]
        st.dataframe(result["table"], use_container_width=True, hide_index=True)
        for note in result["notes"]:
            st.write(f"- {note}")
        output_text = result["table"].to_markdown(index=False) + "\n\n" + "\n".join(result["notes"])
    elif "workload" in st.session_state:
        st.dataframe(st.session_state["workload"], use_container_width=True, hide_index=True)
        output_text = st.session_state["workload"].to_markdown(index=False)
    elif "generic" in st.session_state:
        output_text = st.session_state["generic"]
        st.markdown(output_text)
    else:
        output_text = ""
        st.info("Choose an agent, add context and submit the form to generate an output.")

    if output_text:
        st.download_button("Download output (.md)", data=output_text, file_name="crm-agent-output.md", mime="text/markdown")
        with st.expander("Run metadata"):
            st.json(st.session_state.get("last_run", {}))

st.divider()
st.caption("For a production deployment, add server-side model calls, authentication, authorization, audit logs, secret management, tests and approved connectors.")
