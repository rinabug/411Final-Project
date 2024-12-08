import pytest
from app import app, db
from models import User

# Use the app context for database-related tests
@pytest.fixture
def app_context():
    with app.app_context():  # Ensure app context is active for these tests
        db.create_all()  # Create tables for testing
        yield
        db.drop_all()  # Clean up the database after tests

# Test user creation
def test_create_user(app_context):
    User.create_user('testuser', 'password123')
    user = User.query.filter_by(username='testuser').first()
    
    assert user is not None
    assert user.username == 'testuser'
    assert user.password_hash != 'password123'  # Ensure the password is hashed
    assert User.verify_user('testuser', 'password123') is True
    assert User.verify_user('testuser', 'wrongpassword') is False

# Test creating user with duplicate username
def test_create_user_duplicate_username(app_context):
    # Create a user
    User.create_user('testuser', 'password123')

    # Try to create a user with the same username
    try:
        User.create_user('testuser', 'anotherpassword')
    except Exception as e:
        assert str(e) == 'UNIQUE constraint failed: user.username'

