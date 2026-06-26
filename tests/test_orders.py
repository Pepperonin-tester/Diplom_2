import allure
import pytest
import requests
from constants import BASE_URL, ORDER_ENDPOINT


@allure.title("Создание заказа с авторизацией")
def test_create_order_with_auth(registered_user, valid_ingredient_id):
    with allure.step("Отправляем запрос на создание заказа с токеном авторизации"):
        headers = {"Authorization": registered_user["accessToken"]}
        order_data = {"ingredients": [valid_ingredient_id]}
        response = requests.post(BASE_URL + ORDER_ENDPOINT, json=order_data, headers=headers)
        data = response.json()

    with allure.step("Проверяем, что заказ создан успешно"):
        assert response.status_code == 200
        assert data["success"] is True
        assert "order" in data


@allure.title("Создание заказа без авторизации")
def test_create_order_without_auth(valid_ingredient_id):
    with allure.step("Отправляем запрос на создание заказа без токена авторизации"):
        order_data = {"ingredients": [valid_ingredient_id]}
        response = requests.post(BASE_URL + ORDER_ENDPOINT, json=order_data)
        data = response.json()

    with allure.step("Проверяем, что заказ всё равно создан успешно"):
        assert response.status_code == 200
        assert data["success"] is True
        assert "order" in data


@allure.title("Создание заказа без ингредиентов (авторизация: {with_auth})")
@pytest.mark.parametrize("with_auth", [True, False])
def test_create_order_without_ingredients(registered_user, with_auth):
    with allure.step("Готовим заголовки в зависимости от наличия авторизации"):
        headers = {}
        if with_auth:
            headers = {"Authorization": registered_user["accessToken"]}

    with allure.step("Отправляем запрос на создание заказа без ингредиентов"):
        order_data = {"ingredients": []}
        response = requests.post(BASE_URL + ORDER_ENDPOINT, json=order_data, headers=headers)
        data = response.json()

    with allure.step("Проверяем, что сервер вернул ошибку об отсутствии ингредиентов"):
        assert response.status_code == 400
        assert data["success"] is False
        assert data["message"] == "Ingredient ids must be provided"


@allure.title("Создание заказа с невалидным хешем ингредиента (авторизация: {with_auth})")
@pytest.mark.parametrize("with_auth", [True, False])
def test_create_order_with_invalid_hash(registered_user, with_auth):
    with allure.step("Готовим заголовки в зависимости от наличия авторизации"):
        headers = {}
        if with_auth:
            headers = {"Authorization": registered_user["accessToken"]}

    with allure.step("Отправляем запрос на создание заказа с невалидным id ингредиента"):
        order_data = {"ingredients": ["invalid_ingredient_id"]}
        response = requests.post(BASE_URL + ORDER_ENDPOINT, json=order_data, headers=headers)

    with allure.step("Проверяем, что сервер вернул ошибку 500"):
        assert response.status_code == 500
        assert "Internal Server Error" in response.text
