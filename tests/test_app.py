import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange
    activities.clear()
    activities.update(
        {
            "Chess Club": {
                "description": "Learn strategies",
                "schedule": "Fridays",
                "max_participants": 12,
                "participants": ["michael@mergington.edu"],
            }
        }
    )
    yield


def test_get_activities_returns_the_activity_catalog():
    # Arrange
    client = TestClient(app)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    assert response.json()["Chess Club"]["description"] == "Learn strategies"


def test_signup_for_activity_adds_participant():
    # Arrange
    client = TestClient(app)
    email = "newstudent@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"
    assert email in activities["Chess Club"]["participants"]


def test_duplicate_signup_returns_error():
    # Arrange
    client = TestClient(app)
    duplicate_email = "michael@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": duplicate_email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_participant_removes_the_email_from_activity():
    # Arrange
    client = TestClient(app)
    participant_email = "michael@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Chess Club/unregister",
        params={"email": participant_email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {participant_email} from Chess Club"
    assert participant_email not in activities["Chess Club"]["participants"]
