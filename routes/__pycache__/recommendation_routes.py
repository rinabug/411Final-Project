import json
from flask import Blueprint, request, jsonify
from db import SessionLocal
from models import User, UserRecommendation
from utils.tmdb_utils import get_movie_recommendations_from_tmdb

recommendation_bp = Blueprint('recommendation', __name__)

@recommendation_bp.route('/recommend', methods=['POST'])
def recommend():
    session = SessionLocal()
    data = request.get_json(force=True)
    username = data.get('username')
    genre = data.get('genre')
    age_rating = data.get('age_rating')
    year_range = data.get('year_range')

    if not username or not genre or not age_rating or not year_range:
        session.close()
        return jsonify({"error": "username, genre, age_rating, and year_range are required."}), 400

    user = session.query(User).filter_by(username=username).first()
    if not user:
        session.close()
        return jsonify({"error": "Invalid username."}), 404

    recommendations, status_code = get_movie_recommendations_from_tmdb(genre, age_rating, year_range)
    if status_code != 200:
        session.close()
        return jsonify(recommendations), status_code

    # Store recommendations in the database
    for rec in recommendations:
        watch_providers_json = json.dumps(rec['watch_providers']) if rec['watch_providers'] else None
        new_rec = UserRecommendation(
            user_id=user.id,
            movie_id=rec['movie_id'],
            title=rec['title'],
            overview=rec['overview'],
            release_date=rec['release_date'],
            poster_path=rec['poster_path'],
            watch_providers=watch_providers_json,
            trailer_url=rec['trailer_url']
        )
        session.add(new_rec)
    session.commit()
    session.close()

    return jsonify({"recommendations": recommendations}), 200