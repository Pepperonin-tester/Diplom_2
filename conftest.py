import allure
import pytest
import random
import string
import requests
from constants import REGISTER_URL, INGREDIENTS_URL, DELETE_USER_URL


def generate_random_string(length):
    letters = string.ascii_lowercase + string.digits
    random_chars = random.choices(letters, k=length)
    return ''.join(random_chars)


@pytest.fixture
def random_user_data():
    with allure.step("Генерируем случайные данные пользователя"):
        user_data = {
            "email": f"{generate_random_string(10)}@example.com",
            "password": f"{generate_random_string(8)}",
            "name": f"{generate_random_string(6)}"
        }
        return user_data


@pytest.fixture
def valid_ingredient_id():
    with allure.step("Получаем список ингредиентов и берём валидный id"):
        response = requests.get(INGREDIENTS_URL)
        data = response.json()
        ingredients_list = data["data"]
        return ingredients_list[0]["_id"]


@pytest.fixture
def registered_user(random_user_data):
    with allure.step("Регистрируем нового пользователя через API"):
        response = requests.post(REGISTER_URL, json=random_user_data)
        data = response.json()
        access_token = data["accessToken"]

    yield data

    with allure.step("Удаляем созданного пользователя после теста"):
        requests.delete(DELETE_USER_URL, headers={"Authorization": access_token})


@pytest.fixture
def user_cleanup():
    tokens_to_delete = []

    yield tokens_to_delete

    with allure.step("Удаляем созданных в тесте пользователей"):
        for token in tokens_to_delete:
            requests.delete(DELETE_USER_URL, headers={"Authorization": token})
