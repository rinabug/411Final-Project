import uuid
import json
from flask import Blueprint, request, jsonify
from app.models import User, UserRecommendation
from app.database import session
from app.utils import hash_password

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/create_account', methods=['POST'])
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

@auth_bp.route('/login', methods=['POST'])
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

    # Fetch previously recommended movies for this user
    user_recs = session.query(UserRecommendation).filter_by(user_id=user.id).order_by(UserRecommendation.recommended_at.desc()).all()
    previous_recommendations = []
    for rec in user_recs:
        watch_providers = json.loads(rec.watch_providers) if rec.watch_providers else []
        previous_recommendations.append({
            'movie_id': rec.movie_id,
            'title': rec.title,
            'overview': rec.overview,
            'release_date': rec.release_date,
            'poster_path': rec.poster_path,
            'watch_providers': watch_providers,
            'trailer_url': rec.trailer_url,
            'recommended_at': rec.recommended_at.isoformat()
        })

    return jsonify({
        "message": "Login successful.",
        "previous_recommendations": previous_recommendations
    }), 200

@auth_bp.route('/update_password', methods=['POST'])
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
