import pytest


class TestSignupErrors:
    def test_signup_returns_404_for_nonexistent_activity(self, client, reset_activities):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert "not found" in data["detail"].lower()

    def test_signup_returns_400_for_duplicate_student(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "daniel@mergington.edu"  # Already enrolled

        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"].lower()


class TestUnregisterErrors:
    def test_unregister_returns_404_for_nonexistent_activity(self, client, reset_activities):
        # Arrange
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 404
        data = response.json()
        assert "not found" in data["detail"].lower()

    def test_unregister_returns_400_for_student_not_enrolled(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "notstudent@mergington.edu"  # Not enrolled

        # Act
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert response.status_code == 400
        data = response.json()
        assert "not signed up" in data["detail"].lower()

    def test_unregister_twice_returns_400_on_second_attempt(self, client, reset_activities):
        # Arrange
        activity_name = "Chess Club"
        email = "michael@mergington.edu"

        # Act - First unregister succeeds
        first_response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Act - Second unregister should fail
        second_response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )

        # Assert
        assert first_response.status_code == 200
        assert second_response.status_code == 400
