import json

def test_recommend_no_user(client):
    # Try recommending without user
    payload = {
        "username": "nonexisting",
        "genre": "Action",
        "age_rating": "R",
        "year_range": "2016-2020"
    }
    response = client.post('/recommend', data=json.dumps(payload), content_type='application/json')
    assert response.status_code == 404
    assert "Invalid username." in response.get_data(as_text=True)

def test_recommend_with_user(client):
    # First create a user
    create_payload = {
        "username": "recuser",
        "password": "recpass"
    }
    client.post('/create_account', data=json.dumps(create_payload), content_type='application/json')

    # Now recommend movies
    recommend_payload = {
        "username": "recuser",
        "genre": "Action",
        "age_rating": "PG-13",
        "year_range": "2011-2015"
    }
    response = client.post('/recommend', data=json.dumps(recommend_payload), content_type='application/json')

    # The TMDB call may fail if no API key is set, but assuming you have a valid key:
    # Check status code and structure
    assert response.status_code == 200
    data = response.get_json()
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
