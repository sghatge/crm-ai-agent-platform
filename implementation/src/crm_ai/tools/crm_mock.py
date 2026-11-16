CONTACTS = {
    "C1001": {"contact_id": "C1001", "first_name": "Asha", "last_name": "Mehta", "status": "active"},
    "C1002": {"contact_id": "C1002", "first_name": "Rohan", "last_name": "Iyer", "status": "prospect"},
}


def get_contact(contact_id: str) -> dict | None:
    return CONTACTS.get(contact_id)
