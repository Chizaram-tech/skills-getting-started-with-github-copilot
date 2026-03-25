from fastapi import status


def test_get_activities_returns_data(client):
    # Arrange: nothing special required beyond fixture.

    # Act
    response = client.get('/activities')

    # Assert
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, dict)
    assert 'Chess Club' in data


def test_signup_new_participant(client):
    # Arrange
    activity = 'Chess Club'
    new_email = 'teststudent@mergington.edu'

    # Act
    response = client.post(f'/activities/{activity}/signup', params={'email': new_email})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': f'Signed up {new_email} for {activity}'}

    # Act: verify participant appears
    check = client.get('/activities')
    assert new_email in check.json()[activity]['participants']


def test_signup_duplicate_participant_rejected(client):
    # Arrange
    activity = 'Chess Club'
    existing_email = 'michael@mergington.edu'

    # Act
    response = client.post(f'/activities/{activity}/signup', params={'email': existing_email})

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'already signed up' in response.json().get('detail', '').lower()


def test_unregister_participant(client):
    # Arrange
    activity = 'Chess Club'
    email = 'daniel@mergington.edu'

    # Act
    response = client.delete(f'/activities/{activity}/signup', params={'email': email})

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'message': f'Unregistered {email} from {activity}'}

    # Act: verify removed
    check = client.get('/activities')
    assert email not in check.json()[activity]['participants']


def test_unregister_nonexistent_participant_fails(client):
    # Arrange
    activity = 'Chess Club'
    email = 'notregistered@mergington.edu'

    # Act
    response = client.delete(f'/activities/{activity}/signup', params={'email': email})

    # Assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'not signed up' in response.json().get('detail', '').lower()
