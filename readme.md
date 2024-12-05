# Movie Recommendation App

## Overview
A terminal-based application to fetch movie recommendations using TMDb API.

## Routes
### `/create-account`
- **Method**: POST
- **Request**: `{ "username": "test", "password": "1234" }`
- **Response**: `{ "message": "Account created successfully" }`

### `/movie-recommendations`
- **Method**: GET
- **Query Parameters**: `genre, age_rating, year_range`
- **Response**: JSON with recommended movies