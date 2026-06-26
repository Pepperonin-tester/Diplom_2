import pytest
import random
import string
import requests

from constants import BASE_URL, REGISTER_ENDPOINT, INGREDIENTS_ENDPOINT, DELETE_USER_ENDPOINT


def generate_random_string(length):
    letters = string.ascii_lowercase + string.digits
    random_chars = random.choices(letters, k=length)
    return ''.join(random_chars)

@pytest.fixture
def random_user_data():
    user_data = {
        "email": f"{generate_random_string(10)}@example.com",
        "password": f"{generate_random_string(8)}",
        "name": f"{generate_random_string(6)}"
    }
    return user_data

@pytest.fixture
def valid_ingredient_id():
    response = requests.get(BASE_URL + INGREDIENTS_ENDPOINT)
    data = response.json()
    ingredients_list = data["data"]
    return ingredients_list[0]["_id"]

@pytest.fixture
def registered_user(random_user_data):
    response = requests.post(BASE_URL + REGISTER_ENDPOINT, json=random_user_data)
    data = response.json()
    access_token = data["accessToken"]
    yield data
    requests.delete(BASE_URL + DELETE_USER_ENDPOINT, headers={"Authorization": access_token})
