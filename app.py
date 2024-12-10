import os
import requests
import hashlib
import uuid
import json
import datetime
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')

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
    recommendations = relationship("UserRecommendation", back_populates="user")

# Model to store user's recommended movies
class UserRecommendation(Base):
    __tablename__ = 'user_recommendations'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users_cli.id'), nullable=False)
    movie_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    overview = Column(Text, nullable=True)
    release_date = Column(String(20), nullable=True)
    poster_path = Column(String(255), nullable=True)
    watch_providers = Column(Text, nullable=True)  # JSON string
    trailer_url = Column(String(500), nullable=True)
    recommended_at = Column(DateTime, default=datetime.datetime.utcnow)
    user = relationship("User", back_populates="recommendations")

# Create tables if they don't exist
Base.metadata.create_all(engine)

def hash_password(password, salt):
    """Hash a password with the given salt."""
    pwdhash = hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000
    )
    return pwdhash.hex()

def get_watch_providers(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"
    params = {'api_key': TMDB_API_KEY}
    response = requests.get(url, params=params)
    data = response.json()

    if 'results' in data and 'US' in data['results']:
        providers = data['results']['US']
        streaming_providers = providers.get('flatrate', [])
        streaming_names = [provider['provider_name'] for provider in streaming_providers]
        return streaming_names
    return []

def get_movie_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if 'results' in data:
        for video in data['results']:
            if video['site'] == 'YouTube' and video['type'] == 'Trailer':
                return f"https://www.youtube.com/embed/{video['key']}"
    return None

def get_movie_recommendations_from_tmdb(genre, age_rating, year_range):
    genre_map = {
        "Action": 28,
        "Adventure": 12,
        "Comedy": 35,
        "Drama": 18,
        "Fantasy": 14,
        "Horror": 27,
        "Mystery": 9648,
        "Romance": 10749,
        "Sci-Fi": 878,
        "Thriller": 53
    }

    year_map = {
        "2000-2010": (2000, 2010),
        "2011-2015": (2011, 2015),
        "2016-2020": (2016, 2020),
        "2021-present": (2021, 2024)
    }

    if genre not in genre_map:
        return {"error": "Invalid genre."}, 400
    if year_range not in year_map:
        return {"error": "Invalid year range."}, 400

    start_year, end_year = year_map[year_range]

    url = "https://api.themoviedb.org/3/discover/movie"
    params = {
        'api_key': TMDB_API_KEY,
        'with_genres': genre_map[genre],
        'certification_country': 'US',
        'certification': age_rating,
        'primary_release_date.gte': f'{start_year}-01-01',
        'primary_release_date.lte': f'{end_year}-12-31',
        'sort_by': 'popularity.desc'
    }

    response = requests.get(url, params=params)
    data = response.json()

    # Handle potential API errors
    if response.status_code != 200:
        return {"error": "Failed to fetch recommendations from TMDB."}, 500

    recommendations = []
    if 'results' in data:
        for movie in data['results'][:10]:
            movie_id = movie['id']
            watch_providers = get_watch_providers(movie_id)
            trailer_url = get_movie_trailer(movie_id)
            recommendations.append({
                'movie_id': movie_id,
                'title': movie['title'],
                'overview': movie.get('overview', 'No overview available'),
                'release_date': movie.get('release_date', 'Unknown release date'),
                'poster_path': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None,
                'watch_providers': watch_providers,
                'trailer_url': trailer_url
            })

    return recommendations, 200

app = Flask(__name__)

@app.route("/health", methods=["GET"])
def health_check():
    return "OK", 200


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

@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.get_json(force=True)
    username = data.get('username')
    genre = data.get('genre')
    age_rating = data.get('age_rating')
    year_range = data.get('year_range')

    if not username or not genre or not age_rating or not year_range:
        return jsonify({"error": "username, genre, age_rating, and year_range are required."}), 400

    user = session.query(User).filter_by(username=username).first()
    if not user:
        return jsonify({"error": "Invalid username."}), 404

    recommendations, status_code = get_movie_recommendations_from_tmdb(genre, age_rating, year_range)
    if status_code != 200:
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

    return jsonify({"recommendations": recommendations}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
