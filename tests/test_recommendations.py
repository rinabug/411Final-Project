from unittest.mock import patch
import json

def mocked_tmdb_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, json_data, status_code):
            self.json_data = json_data
            self.status_code = status_code
        def json(self):
            return self.json_data

    # Mock responses based on URL patterns
    if "watch/providers" in args[0]:
        return MockResponse({
            "results": {
                "US": {
                    "flatrate": [{"provider_name": "Netflix"}]
                }
            }
        }, 200)
    elif "/videos" in args[0]:
        return MockResponse({
            "results": [
                {"site": "YouTube", "type": "Trailer", "key": "abcd1234"}
            ]
        }, 200)
    elif "discover/movie" in args[0]:
        return MockResponse({
            "results": [
                {
                    "id": 123,
                    "title": "Test Movie",
                    "overview": "Test overview",
                    "release_date": "2020-01-01",
                    "poster_path": "/testposter.jpg"
                }
            ]
        }, 200)

    return MockResponse({}, 404)

def test_recommendations_with_mocked_tmdb(client):
    # Create a user first
    client.post('/create_account', json={
        "username": "recommend_tester",
        "password": "recommendpass"
    })

    with patch('requests.get', side_effect=mocked_tmdb_get):
        response = client.post('/recommend', json={
            "username": "recommend_tester",
            "genre": "Action",
            "age_rating": "PG-13",
            "year_range": "2016-2020"
        })
        assert response.status_code == 200
        data = response.get_json()
        assert "recommendations" in data
        assert len(data["recommendations"]) == 1
        assert data["recommendations"][0]["title"] == "Test Movie"
