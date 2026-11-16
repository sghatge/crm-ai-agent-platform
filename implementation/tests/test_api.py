from fastapi.testclient import TestClient

from crm_ai.api import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_contact_lookup_found():
    response = client.post("/agents/contact-lookup", json={"contact_id": "C1001"})
    assert response.status_code == 200
    assert response.json()["result"]["first_name"] == "Asha"


def test_unknown_contact():
    response = client.post("/agents/contact-lookup", json={"contact_id": "C9999"})
    assert response.status_code == 200
    assert response.json()["result"] is None


def test_send_message_requires_approval():
    response = client.post("/policy/check?action=send_message&approved=false")
    assert response.status_code == 200
    assert response.json()["allowed"] is False
