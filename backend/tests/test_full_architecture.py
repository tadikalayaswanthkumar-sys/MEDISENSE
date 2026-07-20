import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_full_system_flow():
    email = "single.user@medisense.ai"
    password = "MyHealthPassword123!"
    
    # 1. Register User
    reg_resp = client.post("/api/v1/auth/register", json={
        "name": "Jane Doe",
        "email": email,
        "password": password,
        "role": "Patient"
    })
    assert reg_resp.status_code == 201
    token = reg_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Upload Medical Report
    report_content = b"Fasting Glucose: 110 mg/dL\nTotal Cholesterol: 210 mg/dL\nHemoglobin: 13.5 g/dL"
    files = {"file": ("blood_panel.txt", report_content, "text/plain")}
    data = {"title": "Annual Blood Panel"}
    
    report_resp = client.post("/api/v1/reports/upload", data=data, files=files, headers=headers)
    assert report_resp.status_code == 201
    report_data = report_resp.json()
    assert report_data["title"] == "Annual Blood Panel"
    assert "glucose" in report_data["biomarkers"]
    assert report_data["health_score"] > 0

    # 3. Add Prescription & Log Reminder
    med_resp = client.post("/api/v1/medication/", json={
        "name": "Atorvastatin",
        "dosage": "10mg",
        "frequency": "Once Daily",
        "times": ["08:00 AM"],
        "instructions": "Take with water after breakfast"
    }, headers=headers)
    assert med_resp.status_code == 201
    med_id = med_resp.json()["id"]

    log_resp = client.post(f"/api/v1/medication/{med_id}/log", json={"status": "Taken"}, headers=headers)
    assert log_resp.status_code == 200
    assert log_resp.json()["status"] == "Taken"

    # 4. Fetch User Dashboard Summary
    dash_resp = client.get("/api/v1/dashboard/summary", headers=headers)
    assert dash_resp.status_code == 200
    dash_data = dash_resp.json()
    assert dash_data["reports_count"] >= 1
    assert len(dash_data["active_medicines"]) >= 1
    assert len(dash_data["reminder_history"]) >= 1
