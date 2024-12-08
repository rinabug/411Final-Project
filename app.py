from flask import Flask, jsonify, request, make_response, render_template, redirect
from models import db, User
from routes.account_routes import account_routes
from tmdb_api import TMDBClient
import logging
import os

app = Flask(__name__)

# Load configurations
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(account_routes)

# TMDB Client
tmdb_client = TMDBClient()

# Logging
logging.basicConfig(level=logging.INFO)

# Healthcheck Route
@app.route('/api/health', methods=['GET'])
def healthcheck():
    """Healthcheck route to verify the app is running."""
    return jsonify({'status': 'healthy'}), 200

# Account Management Routes
@app.route('/api/create-account', methods=['POST'])
def create_account():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return make_response(jsonify({'error': 'Username and password are required'}), 400)

    try:
        User.create_user(username, password)
        return jsonify({'message': 'Account created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/api/login', methods=['POST'])
def login():
    """Login and verify username/password."""
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if User.verify_user(username, password):
        return jsonify({'message': 'Login successful'}), 200
    if not password:
        return jsonify({'error': 'Invalid credentials'}), 400 
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/user')
def user_management():
    """Render the user management page."""
    return render_template('user.html')

# Movie Recommendation Routes
@app.route('/api/recommend-movies', methods=['GET'])
def recommend_movies():
    """
    Recommend movies based on genre, rating, and recency.
    """
    genre = request.args.get('genre', '')
    rating = request.args.get('rating', '')
    recency = request.args.get('recency', '')

    # Check for missing parameters
    if not genre or not rating or not recency:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    # Define a mapping for recency ranges
    year_ranges = {
        "2000-2010": (2000, 2010),
        "2011-2015": (2011, 2015),
        "2016-2020": (2016, 2020),
        "2021-present": (2021, 2024)
    }

    # Extract the start and end years from the recency range
    start_year, end_year = year_ranges.get(recency, (2000, 2024))

    # Fetch recommendations from the TMDB API client
    movies = tmdb_client.get_movies_by_genre_rating_and_years(genre, rating, start_year, end_year)
    return jsonify({'recommended_movies': movies}), 200


@app.route('/api/movie-details/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
    """Get detailed information about a movie."""
    movie = tmdb_client.get_movie_details(movie_id)
    return jsonify(movie), 200

@app.route('/api/search-movies', methods=['GET'])
def search_movies():
    """Search for movies by title, including poster URLs."""
    query = request.args.get('query', '')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    results = tmdb_client.search_movies_by_title(query)
    movies = [
        {
            "title": movie.get("title", "Unknown Title"),
            "release_date": movie.get("release_date", "Unknown"),
            "vote_average": movie.get("vote_average", "N/A"),
            "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None,
        }
        for movie in results
    ]
    return jsonify({'search_results': movies}), 200


@app.route('/api/top-rated-movies', methods=['GET'])
def top_rated_movies():
    """Fetch top-rated movies with poster URLs."""
    movies = tmdb_client.get_top_rated_movies()
    return jsonify({'top_rated_movies': movies}), 200

@app.route('/api/now-playing', methods=['GET'])
def now_playing():
    """Fetch now-playing movies with poster URLs."""
    movies = tmdb_client.get_now_playing()
    return jsonify({'now_playing_movies': movies}), 200

@app.route('/')
def index():
    """
    Redirect the root URL to the main frontend at /callback.
    """
    return redirect('/callback')

@app.route('/callback', methods=['GET'])
def callback():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Initialize database
        print("Database initialized.")
    app.run(host='localhost', port=8080, debug=True)
