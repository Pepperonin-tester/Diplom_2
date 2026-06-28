import allure
import pytest
import requests
from constants import REGISTER_URL
from data import USER_ALREADY_EXISTS_MESSAGE, REQUIRED_FIELDS_MESSAGE, STATUS_OK, STATUS_FORBIDDEN


class TestRegister:
    @allure.title("Регистрация уникального пользователя")
    def test_register_unique_user(self, random_user_data, user_cleanup):
        with allure.step("Отправляем запрос на регистрацию уникального пользователя"):
            response = requests.post(REGISTER_URL, json=random_user_data)
            data = response.json()
            user_cleanup.append(data["accessToken"])

        with allure.step("Проверяем, что регистрация прошла успешно"):
            assert response.status_code == STATUS_OK
            assert data["success"] is True
            assert "accessToken" in data

        with allure.step("Проверяем, что данные пользователя совпадают с отправленными"):
            assert data["user"]["email"] == random_user_data["email"]
            assert data["user"]["name"] == random_user_data["name"]

    @allure.title("Регистрация уже существующего пользователя")
    def test_register_existing_user(self, registered_user, random_user_data):
        with allure.step("Повторно отправляем запрос на регистрацию с теми же данными"):
            response = requests.post(REGISTER_URL, json=random_user_data)
            data = response.json()

        with allure.step("Проверяем, что сервер вернул ошибку 'пользователь уже существует'"):
            assert response.status_code == STATUS_FORBIDDEN
            assert data["success"] is False
            assert data["message"] == USER_ALREADY_EXISTS_MESSAGE

    @allure.title("Регистрация с пустым полем: {field}")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_register_with_empty_field(self, random_user_data, field):
        with allure.step(f"Делаем поле '{field}' пустым"):
            random_user_data[field] = ""

        with allure.step("Отправляем запрос на регистрацию"):
            response = requests.post(REGISTER_URL, json=random_user_data)
            data = response.json()

        with allure.step("Проверяем, что сервер вернул ошибку об обязательных полях"):
            assert response.status_code == STATUS_FORBIDDEN
            assert data["success"] is False
            assert data["message"] == REQUIRED_FIELDS_MESSAGE
            