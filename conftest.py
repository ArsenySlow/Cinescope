from faker import Faker
import pytest
import requests

from api.api_manager import ApiManager
from constants import BASE_URL, REGISTER_ENDPOINT
from custom_requester.custom_requester import CustomRequester
from utils.data_generator import DataGenerator

faker = Faker()


@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания общей HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()


@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager с общей сессией.
    """
    return ApiManager(session)


@pytest.fixture(scope="session")
def requester(session):
    """
    Фикстура для создания экземпляра CustomRequester с той же сессией.
    """
    # 👇 Ключевое изменение: используем ту же сессию, что и api_manager
    return CustomRequester(session=session, base_url=BASE_URL)


@pytest.fixture(scope="function")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """
    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="function")
def registered_user(requester, test_user):
    """
    Регистрируем пользователя через тот же requester (в одной сессии),
    и возвращаем его данные.
    """
    # ensure_user_not_exists(requester, test_user["email"])

    response = requester.send_request(
        method="POST",
        endpoint=REGISTER_ENDPOINT,
        data=test_user,
        expected_status=201
    )
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user
