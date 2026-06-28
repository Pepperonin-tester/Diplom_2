import allure
import requests
from constants import ORDER_URL
from data import (
    EMPTY_INGREDIENTS_MESSAGE,
    INTERNAL_SERVER_ERROR_TEXT,
    INVALID_INGREDIENT_ID,
    STATUS_OK,
    STATUS_BAD_REQUEST,
    STATUS_INTERNAL_SERVER_ERROR,
)


class TestOrders:
    @allure.title("Создание заказа с авторизацией")
    def test_create_order_with_auth(self, registered_user, valid_ingredient_id):
        with allure.step("Отправляем запрос на создание заказа с токеном авторизации"):
            headers = {"Authorization": registered_user["accessToken"]}
            order_data = {"ingredients": [valid_ingredient_id]}
            response = requests.post(ORDER_URL, json=order_data, headers=headers)
            data = response.json()

        with allure.step("Проверяем, что заказ создан успешно"):
            assert response.status_code == STATUS_OK
            assert data["success"] is True
            assert "order" in data

    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_auth(self, valid_ingredient_id):
        with allure.step("Отправляем запрос на создание заказа без токена авторизации"):
            order_data = {"ingredients": [valid_ingredient_id]}
            response = requests.post(ORDER_URL, json=order_data)
            data = response.json()

        with allure.step("Проверяем, что заказ всё равно создан успешно"):
            assert response.status_code == STATUS_OK
            assert data["success"] is True
            assert "order" in data

    @allure.title("Создание заказа без ингредиентов, с авторизацией")
    def test_create_order_without_ingredients_with_auth(self, registered_user):
        with allure.step("Отправляем запрос на создание заказа без ингредиентов, с токеном"):
            headers = {"Authorization": registered_user["accessToken"]}
            order_data = {"ingredients": []}
            response = requests.post(ORDER_URL, json=order_data, headers=headers)
            data = response.json()

        with allure.step("Проверяем, что сервер вернул ошибку об отсутствии ингредиентов"):
            assert response.status_code == STATUS_BAD_REQUEST
            assert data["success"] is False
            assert data["message"] == EMPTY_INGREDIENTS_MESSAGE

    @allure.title("Создание заказа без ингредиентов, без авторизации")
    def test_create_order_without_ingredients_without_auth(self):
        with allure.step("Отправляем запрос на создание заказа без ингредиентов, без токена"):
            order_data = {"ingredients": []}
            response = requests.post(ORDER_URL, json=order_data)
            data = response.json()

        with allure.step("Проверяем, что сервер вернул ошибку об отсутствии ингредиентов"):
            assert response.status_code == STATUS_BAD_REQUEST
            assert data["success"] is False
            assert data["message"] == EMPTY_INGREDIENTS_MESSAGE

    @allure.title("Создание заказа с невалидным хешем ингредиента, с авторизацией")
    def test_create_order_with_invalid_hash_with_auth(self, registered_user):
        with allure.step("Отправляем запрос на создание заказа с невалидным id, с токеном"):
            headers = {"Authorization": registered_user["accessToken"]}
            order_data = {"ingredients": [INVALID_INGREDIENT_ID]}
            response = requests.post(ORDER_URL, json=order_data, headers=headers)

        with allure.step("Проверяем, что сервер вернул ошибку 500"):
            assert response.status_code == STATUS_INTERNAL_SERVER_ERROR
            assert INTERNAL_SERVER_ERROR_TEXT in response.text

    @allure.title("Создание заказа с невалидным хешем ингредиента, без авторизации")
    def test_create_order_with_invalid_hash_without_auth(self):
        with allure.step("Отправляем запрос на создание заказа с невалидным id, без токена"):
            order_data = {"ingredients": [INVALID_INGREDIENT_ID]}
            response = requests.post(ORDER_URL, json=order_data)

        with allure.step("Проверяем, что сервер вернул ошибку 500"):
            assert response.status_code == STATUS_INTERNAL_SERVER_ERROR
            assert INTERNAL_SERVER_ERROR_TEXT in response.text
