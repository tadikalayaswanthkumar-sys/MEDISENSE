import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.v1.auth.schemas import UserRegister

client = TestClient(app)

def test_single_user_role_default():
    user_reg = UserRegister(name="Jane Doe", email="jane.doe@medisense.ai", password="Password123!")
    assert user_reg.role == "User"

def test_delete_report_history():
    # 1. Register & login
    email = "delete.test@medisense.ai"
    password = "Password123!"
    client.post("/api/v1/auth/register", json={
        "name": "Delete Test User",
        "email": email,
        "password": password
    })
    
    login_resp = client.post("/api/v1/auth/login", data={"username": email, "password": password})
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Upload dummy report
    files = {'file': ('test_report.png', b'Fasting Glucose: 160 mg/dL', 'image/png')}
    data = {'title': 'Test Report For Delete'}
    upload_resp = client.post("/api/v1/reports/upload", files=files, data=data, headers=headers)
    assert upload_resp.status_code == 201
    report_id = upload_resp.json()["id"]

    # 3. Verify report exists in list
    list_resp = client.get("/api/v1/reports/", headers=headers)
    assert list_resp.status_code == 200
    assert any(r["id"] == report_id for r in list_resp.json())

    # 4. Delete report
    del_resp = client.delete(f"/api/v1/reports/{report_id}", headers=headers)
    assert del_resp.status_code == 200
    assert del_resp.json()["id"] == report_id

    # 5. Verify report is gone
    get_resp = client.get(f"/api/v1/reports/{report_id}", headers=headers)
    assert get_resp.status_code == 404
