from datetime import datetime, timezone
from uuid import uuid4


def audit_event(event_type: str, actor: str, details: dict | None = None) -> dict:
    # Demo only: replace with durable, access-controlled append-only storage.
    return {
        "event_id": str(uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "actor": actor,
        "details": details or {},
    }
