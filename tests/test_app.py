from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_get_activities_includes_participants():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_delete_signup_removes_participant():
    activity = "Chess Club"
    email = "new.student@mergington.edu"

    client.post(f"/activities/{activity}/signup?email={email}")
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    assert response.status_code == 200
    payload = response.json()
    assert "removed" in payload["message"].lower()

    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]
