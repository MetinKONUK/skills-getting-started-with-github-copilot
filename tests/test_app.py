from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    # Should redirect to index.html
    assert str(response.url).endswith("/static/index.html")

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    # Check if we have the activities data
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    # Validate activity structure
    for activity in data.values():
        assert "description" in activity
        assert "schedule" in activity
        assert "max_participants" in activity
        assert "participants" in activity

def test_signup_for_activity():
    # Test successful signup
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Signed up test@mergington.edu for Chess Club"

    # Test signup for non-existent activity
    response = client.post("/activities/NonexistentClub/signup?email=test@mergington.edu")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

    # Test duplicate signup
    response = client.post("/activities/Chess Club/signup?email=test@mergington.edu")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_remove_participant():
    # First add a participant
    email = "testremove@mergington.edu"
    activity = "Chess Club"
    client.post(f"/activities/{activity}/signup?email={email}")

    # Test successful removal
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == f"Removed {email} from {activity}"

    # Test removing non-existent participant
    response = client.delete(f"/activities/{activity}/participants/{email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"

    # Test removing from non-existent activity
    response = client.delete(f"/activities/NonexistentClub/participants/{email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"