import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """Fixture providing FastAPI test client"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to initial state before each test"""
    from src.app import activities
    
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Join the competitive basketball league and tournaments",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Tennis Court": {
            "description": "Learn tennis fundamentals and play matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 8,
            "participants": ["james@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in plays and musicals on stage",
            "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["grace@mergington.edu", "lucas@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and sculpture techniques",
            "schedule": "Mondays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation skills and compete in debates",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 16,
            "participants": ["ryan@mergington.edu", "sophia@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Build and program robots for STEM competitions",
            "schedule": "Fridays, 3:30 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["aiden@mergington.edu"]
        }
    }
    
    # Clear and repopulate
    activities.clear()
    for name, data in original_activities.items():
        activities[name] = data.copy()
        activities[name]["participants"] = data["participants"].copy()
    
    yield
    
    # Cleanup after test
    activities.clear()
    for name, data in original_activities.items():
        activities[name] = data.copy()
        activities[name]["participants"] = data["participants"].copy()
