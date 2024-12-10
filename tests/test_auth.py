import json

def test_create_account_and_login(client):
    # Test create_account
    payload = {
        "username": "testuser",
        "password": "testpass"
    }
    response = client.post('/create_account', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 201

    # Test login
    response = client.post('/login', data=json.dumps(payload), content_type='application/json')
    data = response.get_json()
    assert response.status_code == 200
    assert data["message"] == "Login successful."
