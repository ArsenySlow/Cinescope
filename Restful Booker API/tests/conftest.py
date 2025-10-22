import pytest
import requests
from faker import Faker
from constants import HEADERS, BASE_URL

faker = Faker('ru_RU')


@pytest.fixture(scope="session")
def auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)

    response = requests.post(
        f"{BASE_URL}/auth",
        headers=HEADERS,
        json={"username": "admin", "password": "password123"}
    )
    assert response.status_code == 200, "Ошибка авторизации"
    token = response.json().get("token")
    assert token is not None, "В ответе не оказалось токена"

    session.headers.update({"Cookie": f"token={token}"})
    return session

@pytest.fixture(scope="session")
def no_auth_session():
    session = requests.Session()
    session.headers.update(HEADERS)
    return session

@pytest.fixture
def booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=100000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Cigars"
    }


@pytest.fixture
def modify_data():
    return {
        "firstname": faker.first_name() + '2',
        "lastname": faker.last_name() + '2',
        "totalprice": faker.random_int(min=1, max=99),
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2024-05-05",
            "checkout": "2024-05-08"
        },
        "additionalneeds": "Cigars2"
    }


@pytest.fixture
def error_data():
    return {
        "empty_body": {},
        "empty_fields": {
            "firstname": "",
            "lastname": "",
            "totalprice": 0,
            "depositpaid": 0,
            "bookingdates": {
                "checkin": "",
                "checkout": ""
            },
            "additionalneeds": ""
        },
        "partial_data":
            {
                "firstname": faker.first_name() + '2',
                "lastname": faker.last_name() + '2',
                "totalprice": faker.random_int(min=1, max=99),
            },
        "only_unknown_fields": {
            "firstname2": faker.first_name() + '2',
            "lastname2": faker.last_name() + '2',
            "totalprice2": faker.random_int(min=1, max=99),
            "depositpaid2": False,
            "bookingdates2": {
                "checkin": "2024-05-05",
                "checkout": "2024-05-08"
            },
            "additionalneeds2": "Cigars2"
        },
        "additional_unknown_field": {
            "firstname": faker.first_name() + '2',
            "lastname": faker.last_name() + '2',
            "totalprice": faker.random_int(min=1, max=99),
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2024-05-05",
                "checkout": "2024-05-08"
            },
            "additionalneeds": "Cigars2",
            "additional_field_no_exist": 31
        }
    }
