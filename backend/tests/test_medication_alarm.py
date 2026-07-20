import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_medication_creation_and_deletion():
    # 1. Register & login user
    email = "alarm.test@medisense.ai"
    password = "Password123!"
    client.post("/api/v1/auth/register", json={
        "name": "Alarm Test User",
        "email": email,
        "password": password
    })
    
    login_resp = client.post("/api/v1/auth/login", data={"username": email, "password": password})
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Create prescription alarm
    create_resp = client.post("/api/v1/medication/", json={
        "name": "Atorvastatin",
        "dosage": "10mg",
        "frequency": "Once Daily",
        "times": ["08:00"],
        "instructions": "Take after breakfast"
    }, headers=headers)

    assert create_resp.status_code == 201
    med_id = create_resp.json()["id"]
    assert create_resp.json()["name"] == "Atorvastatin"

    # 3. List medicines
    list_resp = client.get("/api/v1/medication/", headers=headers)
    assert list_resp.status_code == 200
    assert any(m["id"] == med_id for m in list_resp.json())

    # 4. Delete prescription
    del_resp = client.delete(f"/api/v1/medication/{med_id}", headers=headers)
    assert del_resp.status_code == 200
    assert del_resp.json()["id"] == med_id

    # 5. Confirm deletion
    list_after = client.get("/api/v1/medication/", headers=headers)
    assert not any(m["id"] == med_id for m in list_after.json())
