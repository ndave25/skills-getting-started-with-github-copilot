import pytest
from fastapi.testclient import TestClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
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


def test_unregister_participant_removes_the_email_from_activity():
    client = TestClient(app)

    response = client.delete(
        "/activities/Chess Club/unregister?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]
