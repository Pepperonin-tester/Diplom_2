import pytest
import requests
from constants import BASE_URL, ORDER_ENDPOINT


def test_create_order_with_auth(registered_user, valid_ingredient_id):
    headers = {"Authorization": registered_user["accessToken"]}
    order_data = {"ingredients": [valid_ingredient_id]}
    response = requests.post(BASE_URL + ORDER_ENDPOINT, json=order_data, headers=headers)
    data = response.json()
    assert response.status_code == 200
    assert data["success"] is True
    assert "order" in data

def test_create_order_without_auth(valid_ingredient_id):
    order_data = {"ingredients": [valid_ingredient_id]}
    response = requests.post(BASE_URL + ORDER_ENDPOINT, json=order_data)
    data = response.json()
    assert response.status_code == 200
    assert data["success"] is True
    assert "order" in data

@pytest.mark.parametrize("with_auth", [True, False])
def test_create_order_without_ingredients(registered_user, with_auth):
    headers = {}
    if with_auth:
        headers = {"Authorization": registered_user["accessToken"]}
    order_data = {"ingredients": []}
    response = requests.post(BASE_URL + ORDER_ENDPOINT, json=order_data, headers=headers)
    data = response.json()
    assert response.status_code == 400
    assert data["success"] is False
    assert data["message"] == "Ingredient ids must be provided"

@pytest.mark.parametrize("with_auth", [True, False])
def test_create_order_with_invalid_hash(registered_user, with_auth):
    headers = {}
    if with_auth:
        headers = {"Authorization": registered_user["accessToken"]}
    order_data = {"ingredients": ["invalid_ingredient_id"]}
    response = requests.post(BASE_URL + ORDER_ENDPOINT, json=order_data, headers=headers)
    assert response.status_code == 500
    assert "Internal Server Error" in response.text
    