import pytest


class TestRootEndpoint:
    def test_root_redirects_to_index(self, client):
        # Arrange
        # No setup needed

        # Act
        response = client.get("/", follow_redirects=False)

        # Assert
        assert response.status_code == 307
        assert "/static/index.html" in response.headers["location"]


class TestGetActivities:
    def test_get_all_activities_returns_200(self, client, reset_activities):
        # Arrange
        # Activities already loaded via fixture

        # Act
        response = client.get("/activities")

        # Assert
        assert response.status_code == 200
        activities = response.json()
        assert isinstance(activities, dict)
        assert len(activities) > 0

    def test_get_activities_includes_all_required_fields(self, client, reset_activities):
        # Arrange
        required_fields = {
            "description", "schedule",
            "max_participants", "participants"
        }

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name, activity_data in activities.items():
            assert isinstance(activity_name, str)
            assert required_fields.issubset(activity_data.keys())
            assert isinstance(activity_data["participants"], list)
            assert isinstance(activity_data["max_participants"], int)

    def test_get_activities_contains_expected_activities(self, client, reset_activities):
        # Arrange
        expected_activities = [
            "Chess Club", "Programming Class", "Gym Class",
            "Basketball Team", "Tennis Court", "Drama Club",
            "Art Studio", "Debate Team", "Robotics Club"
        ]

        # Act
        response = client.get("/activities")
        activities = response.json()

        # Assert
        for activity_name in expected_activities:
            assert activity_name in activities


class TestSignup:
    def test_signup_successful_with_valid_data(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]

    def test_signup_adds_participant_to_activity(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "newstudent@mergington.edu"

        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        response = client.get("/activities")
        activities = response.json()
        assert email in activities[activity_name]["participants"]

    def test_signup_returns_error_for_duplicate_signup(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "detail" in data
        assert "already signed up" in data["detail"].lower()

    def test_signup_works_with_url_encoded_activity_name(self, client, reset_activities):
        # Arrange
        activity_name = "Tennis Court"
        email = "newstudent@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name.replace(' ', '%20')}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200


class TestUnregister:
    def test_unregister_successful_with_valid_participant(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already a participant

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "Unregistered" in data["message"]

    def test_unregister_removes_participant_from_activity(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act
        client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        response = client.get("/activities")
        activities = response.json()
        assert email not in activities[activity_name]["participants"]

    def test_unregister_allows_participant_to_resign_up(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act - Remove participant
        client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Act - Sign up again
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200
