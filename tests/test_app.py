import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

# Use a valid activity name from the app data
VALID_ACTIVITY = "Chess Club"
VALID_EMAIL = "newstudent@mergington.edu"

# Use an existing participant for duplicate test
EXISTING_EMAIL = activities[VALID_ACTIVITY]["participants"][0]


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert VALID_ACTIVITY in data

def test_signup_activity():
    # Remove VALID_EMAIL if present for a clean test
    if VALID_EMAIL in activities[VALID_ACTIVITY]["participants"]:
        activities[VALID_ACTIVITY]["participants"].remove(VALID_EMAIL)
    response = client.post(f"/activities/{VALID_ACTIVITY}/signup?email={VALID_EMAIL}")
    assert response.status_code == 200
    assert VALID_EMAIL in activities[VALID_ACTIVITY]["participants"]


def test_signup_duplicate():
    response = client.post(f"/activities/{VALID_ACTIVITY}/signup?email={EXISTING_EMAIL}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_invalid_activity():
    response = client.post("/activities/Nonexistent/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
