#tmdb_api.py
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TMDBClient:
    BASE_URL = "https://api.themoviedb.org/3"
    API_KEY = os.getenv('TMDB_API_KEY')

    def __init__(self):
        if not self.API_KEY:
            raise ValueError("TMDB_API_KEY is not set in the environment variables.")

    def get_movies_by_genre_and_rating(self, genre_name, min_rating):
        """
        Fetch movies by genre and minimum rating.

        Args:
            genre_name (str): The name of the genre (e.g., 'Action', 'Drama').
            min_rating (float): The minimum vote average for the movie.

        Returns:
            list: A list of movies matching the criteria.
        """
        genre_map = {
            "Action": 28, "Adventure": 12, "Comedy": 35, "Drama": 18,
            "Fantasy": 14, "Horror": 27, "Mystery": 9648, "Romance": 10749,
            "Sci-Fi": 878, "Thriller": 53
        }
        genre_id = genre_map.get(genre_name)
        if not genre_id:
            return {"error": f"Invalid genre '{genre_name}'"}

        url = f"{self.BASE_URL}/discover/movie"
        params = {
            'api_key': self.API_KEY,
            'with_genres': genre_id,
            'vote_average.gte': min_rating,
            'sort_by': 'popularity.desc'
        }

        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            return {"error": f"Failed to fetch movies: {response.json().get('status_message', 'Unknown error')}"}

    def get_movie_details(self, movie_id):
        """
        Fetch detailed information about a specific movie.

        Args:
            movie_id (int): The ID of the movie.

        Returns:
            dict: Detailed information about the movie.
        """
        url = f"{self.BASE_URL}/movie/{movie_id}"
        params = {'api_key': self.API_KEY}

        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Failed to fetch movie details: {response.json().get('status_message', 'Unknown error')}"}

    def get_movies_by_genre_rating_and_years(self, genre_name, rating, start_year, end_year):
        """Fetch movies by genre, rating, and year range with trailers and posters."""
        genre_map = {
            "Action": 28, "Adventure": 12, "Comedy": 35, "Drama": 18,
            "Fantasy": 14, "Horror": 27, "Mystery": 9648, "Romance": 10749,
            "Sci-Fi": 878, "Thriller": 53
        }
        genre_id = genre_map.get(genre_name)
        if not genre_id:
            return {"error": f"Invalid genre '{genre_name}'"}

        url = f"{self.BASE_URL}/discover/movie"
        params = {
            'api_key': self.API_KEY,
            'with_genres': genre_id,
            'vote_average.gte': rating,
            'primary_release_date.gte': f"{start_year}-01-01",
            'primary_release_date.lte': f"{end_year}-12-31",
            'sort_by': 'popularity.desc'
        }
        response = requests.get(url, params=params)
        if response.status_code != 200:
            return {"error": f"Failed to fetch movies: {response.json().get('status_message', 'Unknown error')}"}

        movies = []
        for movie in response.json().get('results', []):
            trailer_url = self.get_movie_trailer(movie['id'])
            poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None
            movies.append({
                "title": movie.get("title", "Unknown Title"),
                "rating": movie.get("vote_average", "N/A"),
                "genre": genre_name,
                "year": movie.get("release_date", "Unknown").split("-")[0],
                "trailer": trailer_url,
                "poster": poster_url
            })

        return movies

    def get_movie_trailer(self, movie_id):
        url = f"{self.BASE_URL}/movie/{movie_id}/videos"
        params = {'api_key': self.API_KEY}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            for video in response.json().get("results", []):
                if video["site"] == "YouTube" and video["type"] == "Trailer":
                    return f"https://www.youtube.com/embed/{video['key']}"
        return None  # No trailer available

    def search_movies_by_title(self, query):
        """Search movies by title, including poster URLs."""
        url = f"{self.BASE_URL}/search/movie"
        params = {'api_key': self.API_KEY, 'query': query}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('results', [])
        else:
            return {"error": f"Failed to search movies: {response.json().get('status_message', 'Unknown error')}"}


    def get_top_rated_movies(self):
        """Fetch top-rated movies with poster URLs."""
        url = f"{self.BASE_URL}/movie/top_rated"
        params = {'api_key': self.API_KEY, 'language': 'en-US'}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            results = response.json().get('results', [])
            return [
                {
                    "title": movie.get("title", "Unknown Title"),
                    "release_date": movie.get("release_date", "Unknown"),
                    "vote_average": movie.get("vote_average", "N/A"),
                    "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None,
                }
                for movie in results
            ]
        return {"error": f"Failed to fetch top-rated movies: {response.json().get('status_message', 'Unknown error')}"}

    def get_now_playing(self):
        """Fetch now-playing movies with poster URLs."""
        url = f"{self.BASE_URL}/movie/now_playing"
        params = {'api_key': self.API_KEY, 'language': 'en-US', 'region': 'US'}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            results = response.json().get('results', [])
            return [
                {
                    "title": movie.get("title", "Unknown Title"),
                    "release_date": movie.get("release_date", "Unknown"),
                    "vote_average": movie.get("vote_average", "N/A"),
                    "poster": f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get("poster_path") else None,
                }
                for movie in results
            ]
        return {"error": f"Failed to fetch now-playing movies: {response.json().get('status_message', 'Unknown error')}"}
