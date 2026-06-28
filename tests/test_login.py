import allure
import pytest
import requests
from constants import LOGIN_URL
from data import INCORRECT_CREDENTIALS_MESSAGE, STATUS_OK, STATUS_UNAUTHORIZED


class TestLogin:
    @allure.title("Вход под существующим пользователем")
    def test_login_existing_user(self, registered_user, random_user_data):
        with allure.step("Отправляем запрос на вход с верными email и паролем"):
            login_data = {
                "email": random_user_data["email"],
                "password": random_user_data["password"]
            }
            response = requests.post(LOGIN_URL, json=login_data)
            data = response.json()

        with allure.step("Проверяем, что вход выполнен успешно"):
            assert response.status_code == STATUS_OK
            assert data["success"] is True
            assert "accessToken" in data

    @allure.title("Вход с неверным значением поля: {wrong_field}")
    @pytest.mark.parametrize("wrong_field", ["email", "password"])
    def test_login_with_wrong_field(self, registered_user, random_user_data, wrong_field):
        with allure.step(f"Делаем поле '{wrong_field}' неверным"):
            login_data = {
                "email": random_user_data["email"],
                "password": random_user_data["password"]
            }
            login_data[wrong_field] = "wrong_value"

        with allure.step("Отправляем запрос на вход"):
            response = requests.post(LOGIN_URL, json=login_data)
            data = response.json()

        with allure.step("Проверяем, что сервер вернул ошибку авторизации"):
            assert response.status_code == STATUS_UNAUTHORIZED
            assert data["success"] is False
            assert data["message"] == INCORRECT_CREDENTIALS_MESSAGE
