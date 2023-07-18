import os
import requests
from dotenv import load_dotenv
from faker import Faker
import datetime

"""

STRAVA_CLIENT_ID='84739'
STRAVA_CLIENT_SECRET='2c1f395a93ef9b09ed11e33e9970ebc58f800b89'
STRAVA_REFRESH_TOKEN='109596ab46f1e6da290e620f1ea7f37d7d5a53bc'
STRAVA_USERNAME='fhassi'
STRAVA_CITY='Lisbon'
STRAVA_ATHLETE_ID = '19980865'

"""


# Carregar as variáveis de ambiente definidas no arquivo .env
load_dotenv()
athlete_id = os.getenv("STRAVA_ATHLETE_ID")

fake = Faker()


def generate_access_token():
    client_id = os.getenv("STRAVA_CLIENT_ID")
    client_secret = os.getenv("STRAVA_CLIENT_SECRET")
    refresh_token = os.getenv("STRAVA_REFRESH_TOKEN")

    token_url = "https://www.strava.com/api/v3/oauth/token"
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    response = requests.post(token_url, data=payload)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")
        print("Novo token de acesso:", access_token)
        return access_token
    else:
        # Handle error response
        print("Failed to generate access token")
        return None


def make_api_request(endpoint, method="GET", data=None):
    access_token = generate_access_token()
    url = f"https://www.strava.com/api/v3/{endpoint}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers, data=data)
    elif method == "PUT":
        response = requests.put(url, headers=headers, data=data)
    elif method == "DELETE":
        response = requests.delete(url, headers=headers)

    return response


def create_activity(timestamp=None):
    if timestamp:
        start_date_local = timestamp.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        start_date_local = fake.iso8601()

    activity_data = {
        "name": fake.word(),
        "sport_type": fake.random_element(elements=(
            "AlpineSki", "BackcountrySki", "Badminton", "Canoeing", "Crossfit", "EBikeRide", "Elliptical",
            "EMountainBikeRide", "Golf", "GravelRide", "Handcycle", "HighIntensityIntervalTraining", "Hike",
            "IceSkate", "InlineSkate", "Kayaking", "Kitesurf", "MountainBikeRide", "NordicSki", "Pickleball",
            "Pilates", "Racquetball", "Ride", "RockClimbing", "RollerSki", "Rowing", "Run", "Sail", "Skateboard",
            "Snowboard", "Snowshoe", "Soccer", "Squash", "StairStepper", "StandUpPaddling", "Surfing", "Swim",
            "TableTennis", "Tennis", "TrailRun", "Velomobile", "VirtualRide", "VirtualRow", "VirtualRun", "Walk",
            "WeightTraining", "Wheelchair", "Windsurf", "Workout", "Yoga")),
        "start_date_local": start_date_local,
        "elapsed_time": fake.random_int(min=1, max=3600),
        "description": fake.sentence(),
        "distance": fake.random_int(min=1, max=10000),
        "trainer": 0,
        "commute": 0
    }

    response = make_api_request("activities", method="POST", data=activity_data)
    print(activity_data)
    assert response.status_code == 201, "A solicitação não retornou o código de resposta 201 (Created)"

    data = response.json()
    assert "id" in data, "O campo 'id' está faltando na resposta"
    assert isinstance(data["id"], int), "O campo 'id' não é um número inteiro"

    return data["id"]


def get_total_activities():
    access_token = generate_access_token()
    per_page = 200
    total_activities = 0
    page = 1
    has_more_activities = True

    while has_more_activities:
        response = make_api_request(f"athlete/activities?page={page}&per_page={per_page}")
        if response.status_code == 200:
            data = response.json()
            activity_count = len(data)
            total_activities += activity_count
            if activity_count < per_page:
                has_more_activities = False
            else:
                page += 1
        else:
            return None

    return total_activities
