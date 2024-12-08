import pytest
from app import app, db
from models import User
from flask import jsonify

# Test setup using fixture
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///test.db"  # Use a separate test database
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Set up database
        yield client
        with app.app_context():
            db.drop_all()  # Clean up after tests

# Health check test
def test_healthcheck(client):
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json == {'status': 'healthy'}

# Test for account creation
def test_create_account(client):
    response = client.post('/api/create-account', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 201
    assert response.json == {'message': 'Account created successfully'}

    # Test that the user is added to the database
    user = User.query.filter_by(username='testuser').first()
    assert user is not None
    assert user.username == 'testuser'

# Test for login with valid credentials
def test_login_valid(client):
    # First, create the user
    client.post('/api/create-account', json={'username': 'testuser', 'password': 'testpassword'})
    
    response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'testpassword'
    })
    assert response.status_code == 200
    assert response.json == {'message': 'Login successful'}

# Test for login with invalid credentials
def test_login_invalid(client):
    response = client.post('/api/login', json={
        'username': 'nonexistentuser',
        'password': 'wrongpassword'
    })
    assert response.status_code == 401
    assert response.json == {'error': 'Invalid credentials'}

# Test password update with correct old password
def test_update_password_valid(client):
    # First, create the user
    client.post('/api/create-account', json={'username': 'testuser', 'password': 'testpassword'})
    
    # Test password update
    response = client.post('/api/update-password', json={
        'username': 'testuser',
        'old_password': 'testpassword',
        'new_password': 'newpassword123'
    })
    assert response.status_code == 200
    assert response.json == {'message': 'Password updated successfully'}

    # Test login with new password
    response = client.post('/api/login', json={
        'username': 'testuser',
        'password': 'newpassword123'
    })
    assert response.status_code == 200
    assert response.json == {'message': 'Login successful'}

# Test password update with incorrect old password
def test_update_password_invalid_old(client):
    # First, create the user
    client.post('/api/create-account', json={'username': 'testuser', 'password': 'testpassword'})
    
    # Test password update with incorrect old password
    response = client.post('/api/update-password', json={
        'username': 'testuser',
        'old_password': 'wrongpassword',
        'new_password': 'newpassword123'
    })
    assert response.status_code == 401
    assert response.json == {'error': 'Invalid credentials'}

# Test missing username or password in account creation
def test_create_account_missing_fields(client):
    # Missing username
    response = client.post('/api/create-account', json={'password': 'testpassword'})
    assert response.status_code == 400
    assert response.json == {'error': 'Username and password are required'}

    # Missing password
    response = client.post('/api/create-account', json={'username': 'testuser'})
    assert response.status_code == 400
    assert response.json == {'error': 'Username and password are required'}

# Test invalid password during login (e.g., empty or wrong password)
def test_login_empty_password(client):
    response = client.post('/api/login', json={'username': 'testuser', 'password': ''})
    assert response.status_code == 400
    assert response.json == {'error': 'Invalid credentials'}
