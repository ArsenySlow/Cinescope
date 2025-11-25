from faker import Faker
import pytest
import requests

from api.api_manager import ApiManager
from constants.constants import BASE_URL, REGISTER_ENDPOINT
from constants.roles import Roles
from custom_requester.custom_requester import CustomRequester
from entities.user import User
from models.models import TestUser
from resources.user_creds import SuperAdminCreds
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
    random_password = DataGenerator.generate_random_password()

    user_data = TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER.value]
    )
    return user_data

@pytest.fixture(scope="function")
def registered_user(requester, test_user, api_manager):
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
    registered_user = test_user.model_dump()
    registered_user["id"] = response_data["id"]

    # Логинимся и получаем токен
    api_manager.auth_api.authenticate((test_user.email, test_user.password))

    yield registered_user

    # Удаляем пользователя под его токеном
    api_manager.user_api.clean_up_user(registered_user["id"])

@pytest.fixture(scope="function")
def created_movie(super_admin, movie_data):
    """
    Создаём фильм перед тестом и удаляем его после.
    Возвращает словарь с данными фильма.
    """
    # Создаём фильм
    response = super_admin.api.movie_api.create_movie(data=movie_data)
    assert response.status_code == 201, f"Не удалось создать фильм: {response.text}"
    movie = response.json()

    # yield возвращает данные фильма в тест
    yield movie

    # Clean-up после теста
    super_admin.api.movie_api.clean_up_movie(movie["id"])

@pytest.fixture(scope="function")
def super_admin_login(api_manager):
    """
    Авторизация под супер-админом для тестов, где нужен доступ к CRUD операциям.
    """
    api_manager.auth_api.login_as_superadmin()

@pytest.fixture(scope="function")
def movie_data():
    """Генерация данных фильма"""
    name = faker.text(max_nb_chars=15).strip("., ") + ' Cinema'
    return {
        "name": name,
        "price": faker.random_int(min=333, max=335),
        "description": faker.sentence(),
        "location": faker.random_element(["MSK", "SPB"]),
        "published": True,
        "genreId": 1,
    }

@pytest.fixture
def updated_movie_data(created_movie):
    """Генерация данных для обновления фильма на основе уже созданного."""
    original_data = created_movie
    return {
        "name": "Updated " + original_data["name"],
        "price": original_data["price"] + 100,
        "description": original_data["description"] + " Updated description",
        "location": "MSK" if original_data["location"] != "MSK" else "SPB",
        "imageUrl": "https://image.url",
        "published": not original_data["published"],
        "genreId": 1
    }

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()


@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        list(Roles.SUPER_ADMIN.value),
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.model_dump()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        list(Roles.USER.value),
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture
def admin(user_session, super_admin, creation_user_data):
    new_session = user_session()

    admin_user = User(
        creation_user_data['email'],
        creation_user_data['password'],
        list(Roles.ADMIN.value),
        new_session)

    super_admin.api.user_api.create_user(creation_user_data)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user

@pytest.fixture
def registration_user_data():
    random_password = DataGenerator.generate_random_password()

    user_data = TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )
    return user_data