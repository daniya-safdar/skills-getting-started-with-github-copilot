import copy
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import activities, app


client = TestClient(app)


@pytest.fixture(autouse=True)
def restore_activities():
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


def test_unregister_participant_removes_the_participant():
    response = client.delete("/activities/Chess Club/signup?email=michael@mergington.edu")

    assert response.status_code == 200
    assert response.json()["message"] == "Unregistered michael@mergington.edu from Chess Club"
    assert "michael@mergington.edu" not in activities["Chess Club"]["participants"]


def test_unregister_participant_returns_error_when_not_signed_up():
    response = client.delete("/activities/Chess Club/signup?email=missing@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not signed up for this activity"


def test_unregister_participant_returns_error_for_unknown_activity():
    response = client.delete("/activities/Unknown Club/signup?email=michael@mergington.edu")

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
