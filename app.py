from flask import Flask, request, jsonify
import hashlib
import uuid
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Database setup
engine = create_engine('sqlite:///users.db', echo=False)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# User model
class User(Base):
    __tablename__ = 'users_cli'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    salt = Column(String(64), nullable=False)
    password_hash = Column(String(128), nullable=False)

# Create tables if they don't exist
Base.metadata.create_all(engine)

def hash_password(password, salt):
    """Hash a password with the given salt."""
    pwdhash = hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000
    )
    return pwdhash.hex()

app = Flask(__name__)

@app.route('/create_account', methods=['POST'])
def create_account():
    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    # Check if username already exists
    if session.query(User).filter_by(username=username).first():
        return jsonify({"error": "Username already exists."}), 409

    salt = uuid.uuid4().hex
    password_hash = hash_password(password, salt)

    new_user = User(username=username, salt=salt, password_hash=password_hash)
    session.add(new_user)
    session.commit()

    return jsonify({"message": "Account created successfully."}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json(force=True)
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required."}), 400

    user = session.query(User).filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Invalid username or password."}), 401

    password_hash = hash_password(password, user.salt)
    if password_hash != user.password_hash:
        return jsonify({"error": "Invalid username or password."}), 401

    # In a more robust system, you might return a JWT or session token here
    return jsonify({"message": "Login successful."}), 200

@app.route('/update_password', methods=['POST'])
def update_password():
    data = request.get_json(force=True)
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not username or not old_password or not new_password:
        return jsonify({"error": "Username, old_password, and new_password are required."}), 400

    user = session.query(User).filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Invalid username."}), 404

    old_password_hash = hash_password(old_password, user.salt)
    if old_password_hash != user.password_hash:
        return jsonify({"error": "Invalid current password."}), 401

    new_salt = uuid.uuid4().hex
    new_password_hash = hash_password(new_password, new_salt)

    user.salt = new_salt
    user.password_hash = new_password_hash
    session.commit()

    return jsonify({"message": "Password updated successfully."}), 200

if __name__ == '__main__':
    app.run(debug=True)
