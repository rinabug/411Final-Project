def test_create_account(client):
    # Create a new account
    response = client.post('/create_account', json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Account created successfully."

def test_create_account_existing_username(client):
    # Try creating another account with the same username
    response = client.post('/create_account', json={
        "username": "testuser",
        "password": "newpass"
    })
    assert response.status_code == 409
    data = response.get_json()
    assert data["error"] == "Username already exists."

def test_login_success(client):
    # Login with correct credentials
    response = client.post('/login', json={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Login successful."

def test_login_invalid_credentials(client):
    # Login with incorrect password
    response = client.post('/login', json={
        "username": "testuser",
        "password": "wrongpass"
    })
    assert response.status_code == 401
    data = response.get_json()
    assert data["error"] == "Invalid username or password."

def test_update_password_success(client):
    # Update password
    response = client.post('/update_password', json={
        "username": "testuser",
        "old_password": "testpass",
        "new_password": "newtestpass"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Password updated successfully."

    # Login with new password
    response = client.post('/login', json={
        "username": "testuser",
        "password": "newtestpass"
    })
    assert response.status_code == 200
