import pytest
import requests
from constants import BASE_URL, REGISTER_ENDPOINT

def test_register_unique_user(registered_user, random_user_data):
    assert registered_user["success"] is True
    assert "accessToken" in registered_user
    assert registered_user["user"]["email"] == random_user_data["email"]
    assert registered_user["user"]["name"] == random_user_data["name"]

def test_register_existing_user(registered_user, random_user_data):
    response = requests.post(BASE_URL + REGISTER_ENDPOINT, json=random_user_data)
    data = response.json()
    assert response.status_code == 403
    assert data["success"] is False
    assert data["message"] == "User already exists"    

@pytest.mark.parametrize("field", ["email", "password", "name"])
def test_register_with_empty_field(random_user_data, field):
    random_user_data[field] = ""
    response = requests.post(BASE_URL + REGISTER_ENDPOINT, json=random_user_data)
    data = response.json()
    assert response.status_code == 403
    assert data["success"] is False
    assert data["message"] == "Email, password and name are required fields"
