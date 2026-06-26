import pytest
import requests
from conftest import generate_random_string
from constants import BASE_URL, LOGIN_ENDPOINT

def test_login_existing_user(registered_user, random_user_data):
    login_data = {
        "email": random_user_data["email"],
        "password": random_user_data["password"]
    }
    response = requests.post(BASE_URL + LOGIN_ENDPOINT, json=login_data)
    data = response.json()
    assert response.status_code == 200
    assert data["success"] is True
    assert "accessToken" in data

@pytest.mark.parametrize("wrong_field", ["email", "password"])
def test_login_with_wrong_field(registered_user, random_user_data, wrong_field):
    login_data = {
        "email": random_user_data["email"],
        "password": random_user_data["password"]
    }
    login_data[wrong_field] = "wrong_value"
    response = requests.post(BASE_URL + LOGIN_ENDPOINT, json=login_data)
    data = response.json()
    assert response.status_code == 401
    assert data["success"] is False
    assert data["message"] == "email or password are incorrect"
    