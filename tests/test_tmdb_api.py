import pytest
from unittest.mock import patch
from app import app

# Ensure the test client is within the app context
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():  # Ensure the app context is used for these tests
            yield client

# Mocked test for getting movies by genre and rating
@patch('tmdb_api.TMDBClient.get_movies_by_genre_and_rating')
def test_get_movies_by_genre_and_rating(mock_get_movies, client):
    # Mock the API response to return the mocked movie
    mock_get_movies.return_value = [
        {"title": "Mocked Movie", "rating": 8, "genre": "Sci-Fi", "year": "2020", "poster": "mocked_url"}
    ]

    response = client.get('/api/recommend-movies?genre=Sci-Fi&rating=7.5&recency=2016-2020')
    assert response.status_code == 200
    assert 'recommended_movies' in response.json
    assert len(response.json['recommended_movies']) > 0
    assert response.json['recommended_movies'][0]['title'] == "Mocked Movie"

# Test for getting movie details
@patch('tmdb_api.TMDBClient.get_movie_details')
def test_get_movie_details(mock_get_movie_details, client):
    # Mocking the movie details response
    mock_get_movie_details.return_value = {
        'title': 'Mocked Movie',
        'overview': 'This is a mock movie.',
        'release_date': '2020-07-16'
    }

    response = client.get('/api/movie-details/550')  # Example movie ID
    assert response.status_code == 200
    assert 'title' in response.json
    assert response.json['title'] == 'Mocked Movie'
    assert 'overview' in response.json

# Mocked test for getting movies by genre, rating, and years
@patch('tmdb_api.TMDBClient.get_movies_by_genre_rating_and_years')
def test_get_movies_by_genre_rating_and_years(mock_get_movies_by_years, client):
    # Mocking the TMDB API response
    mock_get_movies_by_years.return_value = [
        {"title": "Mocked Action Movie", "rating": 7.5, "genre": "Action", "year": "2020", "poster": "mocked_url"}
    ]

    response = client.get('/api/recommend-movies?genre=Action&rating=7.5&recency=2016-2020')
    assert response.status_code == 200
    assert 'recommended_movies' in response.json
    assert len(response.json['recommended_movies']) > 0
    assert response.json['recommended_movies'][0]['title'] == "Mocked Action Movie"

# Test the recommend-movies route with a valid request
def test_recommend_movies(client):
    # Valid recommendation request
    response = client.get('/api/recommend-movies?genre=Action&rating=7.5&recency=2016-2020')
    assert response.status_code == 200
    assert 'recommended_movies' in response.json
    assert isinstance(response.json['recommended_movies'], list)
    assert len(response.json['recommended_movies']) > 0  # Ensure there's at least one movie in the response

    # Test missing parameters (invalid request)
    response = client.get('/api/recommend-movies')
    assert response.status_code == 400
    assert 'error' in response.json

# Test search movies with a valid title
def test_search_movies(client):
    # Test searching for a valid movie title
    response = client.get('/api/search-movies?query=Inception')
    assert response.status_code == 200
    assert 'search_results' in response.json
    assert isinstance(response.json['search_results'], list)
    assert len(response.json['search_results']) > 0  # Ensure the search results are returned

    # Test for a movie that doesn't exist
    response = client.get('/api/search-movies?query=NonExistentMovie')
    assert response.status_code == 200
    assert 'search_results' in response.json
    assert len(response.json['search_results']) == 0  # No results for a nonexistent movie

# Test for top-rated movies
def test_top_rated_movies(client):
    # Test top-rated movies request
    response = client.get('/api/top-rated-movies')
    assert response.status_code == 200
    assert 'top_rated_movies' in response.json
    assert isinstance(response.json['top_rated_movies'], list)
    assert len(response.json['top_rated_movies']) > 0  # Ensure at least one movie is returned

# Test for now-playing movies
def test_now_playing(client):
    # Test now-playing movies request
    response = client.get('/api/now-playing')
    assert response.status_code == 200
    assert 'now_playing_movies' in response.json
    assert isinstance(response.json['now_playing_movies'], list)
    assert len(response.json['now_playing_movies']) > 0  # Ensure there are now-playing movies in the response
