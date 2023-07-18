from utils import *

#ATHLETE
def test_athlete_endpoint():
    response = make_api_request("athlete")
    assert response.status_code == 200, "The request did not return a 200 (OK) response code"

def test_athlete_response_structure():
    response = make_api_request("athlete")
    assert response.status_code == 200, "The request did not return a 200 (OK) response code"

    # Check if the response contains the expected fields
    expected_fields = [
        "id", "username", "resource_state", "firstname", "lastname", "bio",
        "city", "state", "country", "sex", "premium", "summit",
        "created_at", "updated_at", "badge_type_id", "weight",
        "profile_medium", "profile", "friend", "follower"
    ]
    for field in expected_fields:
        assert field in response.json(), f"The field '{field}' is missing from the response"

    data = response.json()

    # Check the data types of the fields
    assert isinstance(data["id"], int), "The 'id' field is not an integer"
    assert isinstance(data["username"], str), "The 'username' field is not a string"
    assert isinstance(data["resource_state"], int), "The 'resource_state' field is not an integer"
    assert isinstance(data["firstname"], str), "The 'firstname' field is not a string"
    assert isinstance(data["lastname"], str), "The 'lastname' field is not a string"
    assert isinstance(data["bio"], (str, type(None))), "The 'bio' field is not a string or None"
    assert isinstance(data["city"], str), "The 'city' field is not a string"
    assert isinstance(data["state"], str), "The 'state' field is not a string"
    assert isinstance(data["country"], str), "The 'country' field is not a string"
    assert isinstance(data["sex"], str), "The 'sex' field is not a string"
    assert isinstance(data["premium"], bool), "The 'premium' field is not a boolean value"
    assert isinstance(data["summit"], bool), "The 'summit' field is not a boolean value"
    assert isinstance(data["created_at"], str), "The 'created_at' field is not a string"
    assert isinstance(data["updated_at"], str), "The 'updated_at' field is not a string"
    assert isinstance(data["badge_type_id"], int), "The 'badge_type_id' field is not an integer"
    assert isinstance(data["weight"], float), "The 'weight' field is not a floating-point number"
    assert isinstance(data["profile_medium"], str), "The 'profile_medium' field is not a string"
    assert isinstance(data["profile"], str), "The 'profile' field is not a string"
    assert isinstance(data["friend"], (str, type(None))), "The 'friend' field is not a string or None"
    assert isinstance(data["follower"], (str, type(None))), "The 'follower' field is not a string or None"

def test_athlete_field_values():
    response = make_api_request("athlete")
    assert response.status_code == 200, "The request did not return a 200 (OK) response code"

    data = response.json()

    # Check specific field values
    expected_username = os.getenv("STRAVA_USERNAME")
    expected_city = os.getenv("STRAVA_CITY")

    assert data["username"] == expected_username, "The value of the 'username' field does not match the expected value"
    assert data["city"] == expected_city, "The value of the 'city' field does not match the expected value"

def test_athlete_authorization():
    url = "https://www.strava.com/api/v3/athlete"
    response = requests.get(url)
    assert response.status_code == 401, "The request did not return a 401 (Unauthorized) response code"

def test_athlete_authentication_invalid_token():
    url = "https://www.strava.com/api/v3/athlete"

    headers = {
        "Authorization": f"Bearer invalid token"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 401, "The request did not return a 401 (Unauthorized) response code"

def test_athlete_security():
    response = make_api_request("athlete")

    # Verify that the response does not include sensitive information
    assert "access_token" not in response.text, "The response contains the 'access_token' field, which is sensitive information"
    assert "refresh_token" not in response.text, "The response contains the 'refresh_token' field, which is sensitive information"
    assert "password" not in response.text, "The response contains the 'password' field, which is sensitive information"
    assert "email" not in response.text, "The response contains the 'email' field, which is sensitive information"
    assert "credit_card" not in response.text, "The response contains the 'credit_card' field, which is sensitive information"
    assert "social_security_number" not in response.text, "The response contains the 'social_security_number' field, which is sensitive information"
    assert "bank_account_number" not in response.text, "The response contains the 'bank_account_number' field, which is sensitive information"

#ATHLETE_STATS

def test_athlete_stats_endpoint():
    response = make_api_request(f"athletes/{athlete_id}/stats")
    assert response.status_code == 200, "The request did not return a 200 (OK) response code"

def test_inexistent_athlete_stats_endpoint():
    response = make_api_request(f"athletes/01010101010101100101/stats")
    assert response.status_code == 404, "The request did not return a 200 (OK) response code"

def test_athlete_stats_response_structure():
    response = make_api_request(f"athletes/{athlete_id}/stats")
    assert response.status_code == 200, "The request did not return a 200 (OK) response code"

    # Check if the response contains the expected fields
    expected_fields = [
        "biggest_ride_distance", "biggest_climb_elevation_gain",
        "recent_ride_totals", "recent_run_totals", "recent_swim_totals",
        "ytd_ride_totals", "ytd_run_totals", "ytd_swim_totals",
        "all_ride_totals", "all_run_totals", "all_swim_totals"
    ]
    for field in expected_fields:
        assert field in response.json(), f"The field '{field}' is missing from the response"

    data = response.json()

    # Check the data types of the fields
    assert isinstance(data["biggest_ride_distance"], float), "The 'biggest_ride_distance' field is not a floating-point number"
    assert isinstance(data["recent_ride_totals"], dict), "The 'recent_ride_totals' field is not a dictionary"
    assert isinstance(data["recent_run_totals"], dict), "The 'recent_run_totals' field is not a dictionary"
    assert isinstance(data["recent_swim_totals"], dict), "The 'recent_swim_totals' field is not a dictionary"
    assert isinstance(data["ytd_ride_totals"], dict), "The 'ytd_ride_totals' field is not a dictionary"
    assert isinstance(data["ytd_run_totals"], dict), "The 'ytd_run_totals' field is not a dictionary"
    assert isinstance(data["ytd_swim_totals"], dict), "The 'ytd_swim_totals' field is not a dictionary"
    assert isinstance(data["all_ride_totals"], dict), "The 'all_ride_totals' field is not a dictionary"
    assert isinstance(data["all_run_totals"], dict), "The 'all_run_totals' field is not a dictionary"
    assert isinstance(data["all_swim_totals"], dict), "The 'all_swim_totals' field is not a dictionary"

def test_athlete_stats_field_values():
    response = make_api_request(f"athletes/{athlete_id}/stats")
    assert response.status_code == 200, "The request did not return a 200 (OK) response code"

    data = response.json()

    # Check the values of specific fields
    assert data["biggest_ride_distance"] >= 0, "The value of the 'biggest_ride_distance' field is not valid"

    fields = {
        "recent_ride_totals": ["count", "distance", "moving_time", "elapsed_time", "elevation_gain", "achievement_count"],
        "recent_run_totals": ["count", "distance", "moving_time", "elapsed_time", "elevation_gain", "achievement_count"],
        "recent_swim_totals": ["count", "distance", "moving_time", "elapsed_time", "elevation_gain"],
        "ytd_ride_totals": ["count", "distance", "moving_time", "elapsed_time", "elevation_gain"],
        "ytd_run_totals": ["count", "distance", "moving_time", "elapsed_time", "elevation_gain"],
        "ytd_swim_totals": ["count", "distance", "moving_time", "elapsed_time", "elevation_gain"],
        "all_ride_totals": ["count", "distance", "moving_time", "elapsed_time", "elevation_gain"],
        "all_run_totals": ["count", "distance", "moving_time", "elapsed_time", "elevation_gain"],
        "all_swim_totals": ["count", "distance", "moving_time", "elapsed_time", "elevation_gain"],
    }

    for field, subfields in fields.items():
        field_data = data[field]
        for subfield in subfields:
            assert subfield in field_data, f"The field '{field}.{subfield}' is missing from the response"
            assert isinstance(field_data[subfield], (int, float)), f"The value of the field '{field}.{subfield}' is not a valid number"
            assert field_data[subfield] >= 0, f"The value of the field '{field}.{subfield}' is not valid"

def test_athlete_stats_authorization():
    url = f"https://www.strava.com/api/v3/athletes/{athlete_id}/stats"
    response = requests.get(url)
    assert response.status_code == 401, "The request did not return a 401 (Unauthorized) response code"

def test_athlete_stats_authentication_invalid_token():
    url = f"https://www.strava.com/api/v3/athletes/{athlete_id}/stats"

    headers = {
        "Authorization": "Bearer invalid_token"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 401, "The request did not return a 401 (Unauthorized) response code"

def test_athlete_stats_security():
    response = make_api_request(f"athletes/{athlete_id}/stats")

    # Check if the response does not include sensitive information
    assert "access_token" not in response.text, "The response contains the 'access_token' field, which is sensitive information"
    assert "refresh_token" not in response.text, "The response contains the 'refresh_token' field, which is sensitive information"
    assert "password" not in response.text, "The response contains the 'password' field, which is sensitive information"
    assert "email" not in response.text, "The response contains the 'email' field, which is sensitive information"
    assert "credit_card" not in response.text, "The response contains the 'credit_card' field, which is sensitive information"
    assert "social_security_number" not in response.text, "The response contains the 'social_security_number' field, which is sensitive information"
    assert "bank_account_number" not in response.text, "The response contains the 'bank_account_number' field, which is sensitive information"