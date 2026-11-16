def plan_contact_lookup(contact_id: str) -> list[dict]:
    return [{"step": 1, "tool": "get_contact", "arguments": {"contact_id": contact_id}}]
