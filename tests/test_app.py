import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Basketball Team" in data

def test_signup_and_unregister():
    activity = "Basketball Team"
    email = "testuser@mergington.edu"
    # Signup
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200 or response.status_code == 400  # 400 if already signed up
    # Unregister
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 200 or response.status_code == 404  # 404 if not found

def test_signup_duplicate():
    activity = "Soccer Club"
    email = "lucas@mergington.edu"  # Already signed up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_unregister_not_found():
    activity = "Drama Club"
    email = "notfound@mergington.edu"
    response = client.post(f"/activities/{activity}/unregister?email={email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
