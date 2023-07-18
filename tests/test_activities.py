from utils import *

def test_create_activity():
    activity_id = create_activity()
    assert activity_id is not None, "Failed to create activity"

def test_create_activity_with_future_timestamp():
    future_timestamp = datetime.datetime.now() + datetime.timedelta(days=7)
    activity_id = create_activity(timestamp=future_timestamp)
    assert activity_id is None, "Activity created successfully with a future timestamp"

def test_activities_get_activity():
    activity_id = create_activity()

    response = make_api_request(f"activities/{activity_id}")
    assert response.status_code == 200, "The request did not return a 200 (OK) response code"

    data = response.json()
    assert "id" in data, "The 'id' field is missing from the response"
    assert data["id"] == activity_id, "The activity ID in the response does not match the created activity ID"


def test_activities_update_activity():
    activity_id = create_activity()

    update_activity_data = {
        "name": "Updated Activity",
        "description": "Updated description"
    }

    response = make_api_request(f"activities/{activity_id}", method="PUT", data=update_activity_data)
    assert response.status_code == 200, "The request did not return a 200 (OK) response code"

    data = response.json()
    assert "id" in data, "The 'id' field is missing from the response"
    assert data["id"] == activity_id, "The activity ID in the response does not match the updated activity ID"
    assert "name" in data, "The 'name' field is missing from the response"
    assert data["name"] == "Updated Activity", "The activity name in the response does not match the updated name"
    assert "description" in data, "The 'description' field is missing from the response"
    assert data["description"] == "Updated description", "The activity description in the response does not match the updated description"

def test_activities_list_athlete_activities():
    num_activities = fake.random_int(min=2, max=5)

    for _ in range(num_activities):
        create_activity()

    response = make_api_request("athlete/activities")
    assert response.status_code == 200, "The request did not return a 200 (OK) response code"

    data = response.json()
    assert isinstance(data, list), "The response is not a list of activities"
    assert len(data) >= num_activities, "The response does not contain at least the expected number of activities"


def test_activities_required_fields():
    activity_data = {
        "name": fake.word(),
        "start_date_local": fake.iso8601(),
        "elapsed_time": fake.random_int(min=1, max=3600),
        "distance": fake.random_int(min=1, max=10000)
    }

    response = make_api_request("activities", method="POST", data=activity_data)
    assert response.status_code == 400, "The request did not return a 400 (Bad Request) response code"

def test_activities_invalid_fields():
    activity_data = {
        "name": fake.word(),
        "type": "InvalidType",
        "start_date_local": fake.iso8601(),
        "elapsed_time": fake.random_int(min=1, max=3600),
        "description": fake.sentence(),
        "distance": "InvalidDistance",
        "trainer": "InvalidTrainer",
        "commute": "InvalidCommute"
    }

    response = make_api_request("activities", method="POST", data=activity_data)
    assert response.status_code == 400, "The request did not return a 400 (Bad Request) response code"


def test_activities_duplicate_activity():
    original_activity_id = create_activity()

    # Get the data of the original activity
    response = make_api_request(f"activities/{original_activity_id}")
    assert response.status_code == 200, "Failed to get data of the original activity"

    original_activity_data = {
        "name": response.json()["name"],
        "type": response.json()["type"],
        "start_date_local": response.json()["start_date_local"],
        "elapsed_time": response.json()["elapsed_time"],
        "description": response.json()["description"],
        "distance": response.json()["distance"],
        "trainer": response.json()["trainer"],
        "commute": response.json()["commute"]
    }

    # Create the duplicate activity using the data of the original activity
    response = make_api_request("activities", method="POST", data=original_activity_data)
    assert response.status_code == 409, "The request did not return a 409 (Conflict) response code"


def test_activities_authorization():
    url = "https://www.strava.com/api/v3/activities"
    response = requests.get(url)
    assert response.status_code == 401, "The request did not return a 401 (Unauthorized) response code"


def test_activities_authentication_invalid_token():
    url = "https://www.strava.com/api/v3/activities"

    headers = {
        "Authorization": f"Bearer invalid token"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 401, "The request did not return a 401 (Unauthorized) response code"


def test_activities_security():
    response = make_api_request("activities")

    # Check if the response does not include sensitive information
    assert "access_token" not in response.text, "The response contains the 'access_token' field, which is sensitive information"
    assert "refresh_token" not in response.text, "The response contains the 'refresh_token' field, which is sensitive information"
    assert "password" not in response.text, "The response contains the 'password' field, which is sensitive information"
    assert "email" not in response.text, "The response contains the 'email' field, which is sensitive information"
    assert "credit_card" not in response.text, "The response contains the 'credit_card' field, which is sensitive information"
    assert "social_security_number" not in response.text, "The response contains the 'social_security_number' field, which is sensitive information"
    assert "bank_account_number" not in response.text, "The response contains the 'bank_account_number' field, which is sensitive information"


#athlete/activities

def test_athlete_activities_list_athlete_activities_endpoint():
    response = make_api_request("athlete/activities")
    assert response.status_code == 200, "The request did not return a 200 (OK) response code"


def test_athlete_activities_list_athlete_activities_response_structure():
    response = make_api_request("athlete/activities")
    assert response.status_code == 200, "The request did not return a 200 (OK) response code"

    data = response.json()
    assert isinstance(data, list), "The response is not a list of activities"

    if len(data) > 0:
        # Check if the response contains the expected fields for at least one activity
        expected_fields = [
            "id", "name", "type", "start_date", "distance", "elapsed_time"
        ]
        for field in expected_fields:
            assert field in data[0], f"The field '{field}' is missing from the response for the first activity"


def test_list_athlete_activities_pagination():
    per_page = fake.random_int(min=2, max=99)

    total_activities = get_total_activities()

    if total_activities < 10:
        num_activities = fake.random_int(min=2, max=5)

        for _ in range(num_activities):
            create_activity()
    else:
        num_activities = 0

    # Retrieve the first page of activities
    response = make_api_request(f"athlete/activities?per_page={per_page}")
    assert response.status_code == 200, "The request did not return a 200 (OK) response code"

    data = response.json()
    assert isinstance(data, list), "The response is not a list of activities"
    assert len(data) <= per_page, "The response contains more activities than expected for the first page"

    # Calculate the total number of pages based on the number of activities
    total_pages = (total_activities + per_page - 1) // per_page

    if total_pages > 1:
        # Retrieve the remaining pages of activities
        for page in range(2, total_pages + 1):
            response = make_api_request(f"athlete/activities?page={page}&per_page={per_page}")
            assert response.status_code == 200, "The request did not return a 200 (OK) response code"

            data = response.json()
            assert isinstance(data, list), "The response is not a list of activities"
            assert len(data) <= per_page, f"The response contains more activities than expected for page {page}"


def test_list_athlete_activities_filtering():
    # Create activities with different timestamps
    current_time = datetime.datetime.now()
    activity_timestamps = [
        current_time - datetime.timedelta(days=7),
        current_time - datetime.timedelta(days=3),
        current_time - datetime.timedelta(days=1),
        current_time
    ]

    for timestamp in activity_timestamps:
        create_activity(timestamp)

    # Filter activities after a specific timestamp
    after_timestamp = current_time - datetime.timedelta(days=4)
    response = make_api_request(f"athlete/activities?after={int(after_timestamp.timestamp())}&page=1")
    assert response.status_code == 200, "The request did not return a 200 (OK) response code"

    data = response.json()
    assert isinstance(data, list), "The response is not a list of activities"

    # Check if all activities in the response are after the specified timestamp
    for activity in data:
        activity_timestamp = datetime.datetime.strptime(activity["start_date"], "%Y-%m-%dT%H:%M:%SZ")
        assert activity_timestamp > after_timestamp, "An activity in the response is not after the specified timestamp"

    # Filter activities before a specific timestamp
    before_timestamp = current_time - datetime.timedelta(days=2)
    response = make_api_request(f"athlete/activities?before={int(before_timestamp.timestamp())}&page=1")
    assert response.status_code == 200, "The request did not return a 200 (OK) response code"

    data = response.json()
    assert isinstance(data, list), "The response is not a list of activities"

    # Check if all activities in the response are before the specified timestamp
    for activity in data:
        activity_timestamp = datetime.datetime.strptime(activity["start_date"], "%Y-%m-%dT%H:%M:%SZ")
        assert activity_timestamp < before_timestamp, "An activity in the response is not before the specified timestamp"


def test_per_page_limit():
    max_per_page = 200

    # Test with the maximum allowed value
    response = make_api_request(f"athlete/activities?per_page={max_per_page}")
    assert response.status_code == 200, "The request did not return a 200 (OK) response code"

    # Test with a value exceeding the limit
    invalid_per_page = max_per_page + 1
    response = make_api_request(f"athlete/activities?per_page={invalid_per_page}")
    assert response.status_code == 400, "The request did not return a 400 (Bad Request) response code"

    data = response.json()
    assert "message" in data, "The response does not contain the 'message' field"
    assert "errors" in data, "The response does not contain the 'errors' field"

    errors = data["errors"]
    assert isinstance(errors, list), "The 'errors' field is not a list"
    assert len(errors) == 1, "The 'errors' field does not contain exactly one error"

    error = errors[0]
    assert "resource" in error, "The error does not contain the 'resource' field"
    assert error["resource"] == "Application", "The 'resource' field is not 'Application'"
    assert "field" in error, "The error does not contain the 'field' field"
    assert error["field"] == "per page", "The 'field' field is not 'per page'"
    assert "code" in error, "The error does not contain the 'code' field"
    assert error["code"] == "limit exceeded", "The 'code' field is not 'limit exceeded'"
