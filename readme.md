# Movie Recommendation App

## Overview
This Flask-based web application that uses the TMDB API and provides:
1. Account Management (Create, Login, and Update Password).
2. Movie Recommendations via The Movie Database (TMDB) API.
3. Frontend Interface for easy interaction.
4. Docker Support for containerized deployment.

## Setup Instructions
1. Install Dependencies: create virtual enviroment and install required dependencies:
```
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```
2. Environment Variables: Create a .env file in the project root directory with the following content
```
DATABASE_URL=sqlite:///movies.db
TMDB_API_KEY=your_tmdb_api_key_here
```
    To get TMDB API Key, register at: [TMDB](https://developer.themoviedb.org/docs/getting-started) 
    
3. SQL Database Setup: initialize it by running
```
bash sql/init_db.sh
```
4. Run the App
```
python app.py
```
The app will be available at: http://localhost:8080
5. Docker Deployment: to run app using docker
```
docker build -t movie_app .
docker run -p 8080:5000 movie_app
```

## Routes
1. Health Check
### `/api/health`
- **Method**: GET
- **Purpose**: Verify app is running.
- **Response**: `{"status": "healthy"}`

2. Create Account
### `/api/create-account`
- **Method**: POST
- **Request**: `{"username": "your_username", "password": "your_password"}`
- **Response**: `{"message": "Account created successfully"}`

3. Login
### `/api/login`
- **Method**: POST
- **Request**: `{"username": "your_username", "password": "your_password"}`
- **Response**: `{"message": "Login successful"}`

4. Update Password
### `/api/update-password`
- **Method**: POST
- **Request**: `{"username": "your_username", "password": "your_old_password", "new_password": "your_new_password"}`
- **Response**: `{"message": "Password updated successfully"}`

5. Recommend Movies
### `/api/recommend-movies`
- **Method**: GET
- **Request Parameters**:
    - genre: e.g., "Action"
    - rating: e.g., 7.0
    - recency: e.g., "2016-2020"
- **Response**: `{
  "recommended_movies": [
    {
      "title": "Movie Title",
      "rating": 8.5,
      "genre": "Action",
      "year": "2019",
      "trailer": "https://www.youtube.com/embed/xyz",
      "poster": "https://image.tmdb.org/t/p/w500/path_to_poster.jpg"
    }
  ]
}`

6. Movie Details
### `/api/movie-details/<int:movie_id>`
- **Method**: GET
- **Response**: `{
  "title": "Movie Title",
  "overview": "Movie description",
  "release_date": "2020-01-01",
  "vote_average": 8.2
}`

7. Search Movies
### `/api/search-movies`
- **Method**: GET
- **Request Parameters**:
    - query: Movie title keyword
- **Response**: `{
  "search_results": [
    {
      "title": "Inception",
      "release_date": "2010-07-16",
      "vote_average": 8.8,
      "poster": "https://image.tmdb.org/t/p/w500/path_to_poster.jpg"
    }
  ]
}`

8. Top-Rated Movies
### `/api/top-rated-movies`
- **Method**: GET
- **Response**: `{
  "top_rated_movies": [
    {
      "title": "The Shawshank Redemption",
      "release_date": "1994-09-23",
      "vote_average": 9.3,
      "poster": "https://image.tmdb.org/t/p/w500/path_to_poster.jpg"
    }
  ]
}`

9. Now-Playing Movies
### `/api/now-playing`
- **Method**: GET
- **Response**: `{
  "now_playing_movies": [
    {
      "title": "Dune: Part Two",
      "release_date": "2024-03-01",
      "vote_average": 8.5,
      "poster": "https://image.tmdb.org/t/p/w500/path_to_poster.jpg"
    }
  ]
}`

## Simple Frontend Interface
### Pages
1. Movie Recommender
    - Path: http://localhost:8080/callback
    - File: templates/index.html
    - Interact with movie recommendation features

2. User Management
    - Path: http://localhost:8080/user
    - File: templates/user.html
    - Create accounts, log in, and update passwords.

## Project Structure
.
├── app.py
├── models.py
├── tmdb_api.py
├── routes/
│   ├──__ init__.py 
│   └── account_routes.py
├── templates/
│   ├── index.html
│   └── user.html
├── static/
│   ├── styles.css
│   ├── scripts.js
│   └── user.js
├── sql/
│   ├── create_users_table.sql
│   └── init_db.sh
├── Dockerfile
├── requirements.txt
├── .env
└── tests/
    ├── __ init__.py
    ├── test_app.py
    ├── test_models.py
    └── test_tmdb_api.py

## Testing

- Install `pytest` if not installed:
    `pip install pytest`
- Run all tests:
    `pytest`
