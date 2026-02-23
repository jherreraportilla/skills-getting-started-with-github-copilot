import pytest


class TestActivityCapacity:
    def test_activity_shows_correct_spots_remaining(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        max_participants = 12
        current_participants = 2
        expected_spots = max_participants - current_participants

        # Act
        response = client.get("/activities")
        activities = response.json()
        activity = activities[activity_name]
        spots_remaining = (
            activity["max_participants"] -
            len(activity["participants"])
        )

        # Assert
        assert spots_remaining == expected_spots

    def test_signup_increases_participant_count(self, client, reset_activities):
        # Arrange
        activity_name = "Basketball Team"
        email = "newstudent@mergington.edu"
        response_before = client.get("/activities")
        count_before = len(response_before.json()[activity_name]["participants"])

        # Act
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        response_after = client.get("/activities")
        count_after = len(response_after.json()[activity_name]["participants"])

        # Assert
        assert count_after == count_before + 1

    def test_unregister_decreases_participant_count(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        response_before = client.get("/activities")
        count_before = len(response_before.json()[activity_name]["participants"])

        # Act
        client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        response_after = client.get("/activities")
        count_after = len(response_after.json()[activity_name]["participants"])

        # Assert
        assert count_after == count_before - 1

    def test_can_signup_when_below_capacity(self, client, reset_activities):
        # Arrange
        activity_name = "Robotics Club"  # max 20, currently 1
        email = "newstudent1@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 200

    def test_multiple_students_can_signup_for_same_activity(self, client, reset_activities):
        # Arrange
        activity_name = "Art Studio"
        emails = [
            "student1@mergington.edu",
            "student2@mergington.edu",
            "student3@mergington.edu"
        ]

        # Act
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200

        # Assert
        response = client.get("/activities")
        activity = response.json()[activity_name]
        for email in emails:
            assert email in activity["participants"]
