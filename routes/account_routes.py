# routes/account_routes.py
from flask import Blueprint, request, jsonify
from models import User, db
from bcrypt import gensalt, hashpw

account_routes = Blueprint('account_routes', __name__)

@account_routes.route('/api/update-password', methods=['POST'])
def update_password():
    """Update the password for an existing user."""
    data = request.json
    username = data.get('username')
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not User.verify_user(username, old_password):
        return jsonify({'error': 'Invalid credentials'}), 401

    try:
        user = User.query.filter_by(username=username).first()
        salt = gensalt().decode()
        hashed_pw = hashpw(new_password.encode(), salt.encode()).decode()
        user.password_hash = hashed_pw
        user.salt = salt
        db.session.commit()
        return jsonify({'message': 'Password updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500