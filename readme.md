# Movie Recommendation Application

## Overview
This application is a movie recommendation platform where users can create an account, log in, and receive personalized movie suggestions based on genre, age rating, and year range preferences. It integrates with The Movie Database (TMDB) API to fetch movies and provide additional details like trailers and watch providers.

This Flask-based web application that uses the TMDB API and provides:

Account Management (Create, Login, and Update Password).
Movie Recommendations via The Movie Database (TMDB) API.
Frontend Interface for easy interaction.
Docker Support for containerized deployment.

---

## Routes

### 1. **Health Check**
- **Route**: `/health`
- **Request Type**: GET
- **Purpose**: Verifies that the server is running.
- **Request Format**: None
- **Response Format**: 
  - Code: `200`
  - Content: `"OK"`

---

### 2. **Create Account**
- **Route**: `/create_account`
- **Request Type**: POST
- **Purpose**: Creates a new user account.
- **Request Body**:
  - `username` (String): The user's chosen username.
  - `password` (String): The user's chosen password.
- **Response Format**:
  - Success Response Example:
    ```json
    {
      "message": "Account created successfully"
    }
    ```
  - Error Response Example:
    ```json
    {
      "error": "Username already exists."
    }
    ```
- **Example Request**:
  ```json
  {
    "username": "newuser123",
    "password": "securepassword"
  }
  ```
- **Example Response**:
  ```json
  {
    "message": "Account created successfully"
  }
  ```

---

### 3. **Login**
- **Route**: `/login`
- **Request Type**: POST
- **Purpose**: Logs in the user and retrieves previous recommendations.
- **Request Body**:
  - `username` (String): The user's username.
  - `password` (String): The user's password.
- **Response Format**:
  - Success Response Example:
    ```json
    {
      "message": "Login successful.",
      "previous_recommendations": [
        {
          "movie_id": 12345,
          "title": "Example Movie",
          "overview": "This is a sample overview.",
          "release_date": "2022-01-01",
          "poster_path": "https://example.com/poster.jpg",
          "watch_providers": ["Netflix", "Hulu"],
          "trailer_url": "https://youtube.com/trailer",
          "recommended_at": "2024-12-10T00:00:00Z"
        }
      ]
    }
    ```
  - Error Response Example:
    ```json
    {
      "error": "Invalid username or password."
    }
    ```
- **Example Request**:
  ```json
  {
    "username": "newuser123",
    "password": "securepassword"
  }
  ```

---

### 4. **Update Password**
- **Route**: `/update_password`
- **Request Type**: POST
- **Purpose**: Updates the user's password.
- **Request Body**:
  - `username` (String): The user's username.
  - `old_password` (String): The user's current password.
  - `new_password` (String): The new password.
- **Response Format**:
  - Success Response Example:
    ```json
    {
      "message": "Password updated successfully."
    }
    ```
  - Error Response Example:
    ```json
    {
      "error": "Invalid current password."
    }
    ```
- **Example Request**:
  ```json
  {
    "username": "newuser123",
    "old_password": "oldpassword",
    "new_password": "newsecurepassword"
  }
  ```

---

### 5. **Get Movie Recommendations**
- **Route**: `/recommend`
- **Request Type**: POST
- **Purpose**: Fetches personalized movie recommendations based on user preferences.
- **Request Body**:
  - `username` (String): The user's username.
  - `genre` (String): Movie genre (e.g., "Action", "Drama").
  - `age_rating` (String): Age rating (e.g., "PG", "R").
  - `year_range` (String): Year range (e.g., "2000-2010").
- **Response Format**:
  - Success Response Example:
    ```json
    {
      "recommendations": [
        {
          "movie_id": 12345,
          "title": "Example Movie",
          "overview": "This is a sample overview.",
          "release_date": "2022-01-01",
          "poster_path": "https://example.com/poster.jpg",
          "watch_providers": ["Netflix", "Hulu"],
          "trailer_url": "https://youtube.com/trailer"
        }
      ]
    }
    ```
  - Error Response Example:
    ```json
    {
      "error": "Invalid genre."
    }
    ```
- **Example Request**:
  ```json
  {
    "username": "newuser123",
    "genre": "Action",
    "age_rating": "PG",
    "year_range": "2000-2010"
  }
  ```

---

### Error Handling
All error responses are returned as JSON with a descriptive error message and appropriate HTTP status code.

---

