from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Movie Model
class MovieModel:
    def __init__(self):
        # This would be where you connect to a database or an external movie API
        self.movies = []

    def create_movie(self, title, genre, rating, year):
        new_movie = {"title": title, "genre": genre, "rating": rating, "year": year}
        self.movies.append(new_movie)

    def get_movie_by_id(self, movie_id):
        try:
            return self.movies[movie_id]
        except IndexError:
            raise Exception("Movie not found")

    def get_all_movies(self):
        return self.movies

    def delete_movie(self, movie_id):
        try:
            self.movies.pop(movie_id)
        except IndexError:
            raise Exception("Movie not found")

movie_model = MovieModel()

####################################################
#
# Healthcheck
#
####################################################

@app.route('/api/health', methods=['GET'])
def healthcheck() -> Response:
    """
    Health check route to verify the service is running.
    """
    return make_response(jsonify({'status': 'healthy'}), 200)


##########################################################
#
# Movies
#
##########################################################

@app.route('/api/create-movie', methods=['POST'])
def add_movie() -> Response:
    """
    Route to add a new movie to the database.

    Expected JSON Input:
        - title (str): The title of the movie.
        - genre (str): The genre of the movie.
        - rating (float): The rating of the movie (0-10).
        - year (int): The year the movie was released.

    Returns:
        JSON response indicating the success of the movie addition.
    """
    try:
        data = request.get_json()
        title = data.get('title')
        genre = data.get('genre')
        rating = data.get('rating')
        year = data.get('year')

        if not title or not genre or rating is None or year is None:
            return make_response(jsonify({'error': 'Invalid input, all fields are required'}), 400)

        movie_model.create_movie(title, genre, rating, year)

        return make_response(jsonify({'status': 'success', 'movie': title}), 201)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/api/delete-movie/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id: int) -> Response:
    """
    Route to delete a movie by its ID.

    Path Parameter:
        - movie_id (int): The ID of the movie to delete.

    Returns:
        JSON response indicating success or error message.
    """
    try:
        movie_model.delete_movie(movie_id)
        return make_response(jsonify({'status': 'success'}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/api/get-movie-by-id/<int:movie_id>', methods=['GET'])
def get_movie_by_id(movie_id: int) -> Response:
    """
    Route to get a movie by its ID.

    Path Parameter:
        - movie_id (int): The ID of the movie.

    Returns:
        JSON response with the movie details or error message.
    """
    try:
        movie = movie_model.get_movie_by_id(movie_id)
        return make_response(jsonify({'status': 'success', 'movie': movie}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


@app.route('/api/get-all-movies', methods=['GET'])
def get_all_movies() -> Response:
    """
    Route to get all movies.

    Returns:
        JSON response with a list of all movies.
    """
    try:
        movies = movie_model.get_all_movies()
        return make_response(jsonify({'status': 'success', 'movies': movies}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


############################################################
#
# Movie Recommendations
#
############################################################

@app.route('/api/recommend-movies', methods=['GET'])
def recommend_movies() -> Response:
    """
    Route to recommend movies based on genre or rating.
    
    Query Parameters:
        - genre (str): The genre of movies to recommend.
        - rating (float): The minimum rating of movies to recommend.
    
    Returns:
        JSON response with a list of recommended movies.
    """
    try:
        genre = request.args.get('genre')
        rating = request.args.get('rating', type=float)

        recommended_movies = [movie for movie in movie_model.get_all_movies() 
                              if (genre is None or movie['genre'].lower() == genre.lower()) and
                                 (rating is None or movie['rating'] >= rating)]

        return make_response(jsonify({'status': 'success', 'recommended_movies': recommended_movies}), 200)
    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
