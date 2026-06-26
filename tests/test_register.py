import allure
import pytest
import requests
from constants import BASE_URL, REGISTER_ENDPOINT


@allure.title("Регистрация уникального пользователя")
def test_register_unique_user(registered_user, random_user_data):
    with allure.step("Проверяем, что регистрация прошла успешно"):
        assert registered_user["success"] is True
        assert "accessToken" in registered_user

    with allure.step("Проверяем, что данные пользователя совпадают с отправленными"):
        assert registered_user["user"]["email"] == random_user_data["email"]
        assert registered_user["user"]["name"] == random_user_data["name"]


@allure.title("Регистрация уже существующего пользователя")
def test_register_existing_user(registered_user, random_user_data):
    with allure.step("Повторно отправляем запрос на регистрацию с теми же данными"):
        response = requests.post(BASE_URL + REGISTER_ENDPOINT, json=random_user_data)
        data = response.json()

    with allure.step("Проверяем, что сервер вернул ошибку 'пользователь уже существует'"):
        assert response.status_code == 403
        assert data["success"] is False
        assert data["message"] == "User already exists"


@allure.title("Регистрация с пустым полем: {field}")
@pytest.mark.parametrize("field", ["email", "password", "name"])
def test_register_with_empty_field(random_user_data, field):
    with allure.step(f"Делаем поле '{field}' пустым"):
        random_user_data[field] = ""

    with allure.step("Отправляем запрос на регистрацию"):
        response = requests.post(BASE_URL + REGISTER_ENDPOINT, json=random_user_data)
        data = response.json()

    with allure.step("Проверяем, что сервер вернул ошибку об обязательных полях"):
        assert response.status_code == 403
        assert data["success"] is False
        assert data["message"] == "Email, password and name are required fields"
        