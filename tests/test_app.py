import pytest


# ---------------------------------------------------------------------------
# GET /activities
# ---------------------------------------------------------------------------

def test_get_activities_returns_all(client):
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


# ---------------------------------------------------------------------------
# POST /activities/{activity_name}/signup
# ---------------------------------------------------------------------------

def test_signup_success(client):
    # Arrange
    activity = "Chess Club"
    email = "new@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for {activity}"}


def test_signup_duplicate_email(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already in Chess Club

    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_activity_full(client):
    # Arrange — fill Chess Club (max 12) with unique emails
    activity = "Chess Club"
    for i in range(10):
        res = client.post(f"/activities/{activity}/signup?email=filler{i}@mergington.edu")
        assert res.status_code == 200
    # Act — one more should be rejected
    response = client.post(f"/activities/{activity}/signup?email=overflow@mergington.edu")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"


def test_signup_unknown_activity(client):
    # Arrange — no setup needed

    # Act
    response = client.post("/activities/Nonexistent Club/signup?email=x@mergington.edu")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


# ---------------------------------------------------------------------------
# DELETE /activities/{activity_name}/signup
# ---------------------------------------------------------------------------

def test_unregister_success(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already in Chess Club

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from {activity}"}


def test_unregister_not_registered(client):
    # Arrange
    activity = "Chess Club"
    email = "nothere@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student not registered for this activity"


def test_unregister_unknown_activity(client):
    # Arrange — no setup needed

    # Act
    response = client.delete("/activities/Nonexistent Club/signup?email=x@mergington.edu")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
