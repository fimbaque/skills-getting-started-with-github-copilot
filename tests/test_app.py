from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_get_activities():
    res = client.get('/activities')
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert 'Chess Club' in data


def test_signup_and_duplicate_handling():
    # Use a test email and activity
    activity = 'Chess Club'
    email = 'testuser@example.com'

    # Ensure email not present initially
    if email in activities[activity]['participants']:
        activities[activity]['participants'].remove(email)

    # Signup
    res = client.post(f"/activities/{activity}/signup?email={email}")
    assert res.status_code == 200
    assert res.json().get('message')
    assert email in activities[activity]['participants']

    # Duplicate signup should return 400
    res2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert res2.status_code == 400

    # Cleanup
    if email in activities[activity]['participants']:
        activities[activity]['participants'].remove(email)


def test_delete_participant():
    activity = 'Chess Club'
    email = 'delete-me@example.com'

    # Ensure participant exists
    if email not in activities[activity]['participants']:
        activities[activity]['participants'].append(email)

    # Delete the participant
    res = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res.status_code == 200
    assert email not in activities[activity]['participants']

    # Deleting again should return 404
    res2 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert res2.status_code == 404
