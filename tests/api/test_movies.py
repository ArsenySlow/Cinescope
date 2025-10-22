import pytest
import requests
from constants import HEADERS, MOVIES_ENDPOINT

BASE_URL = 'https://api.dev-cinescope.coconutqa.ru'
PARAMS = 'pageSize=10&page=1&minPrice=1&maxPrice=1000&locations=SPB&published=true&genreId=1&createdAt=asc'

class TestMoviesAPI:
    def test_getting_movies_no_params(self):
        # URL для регистрации
        movies_url = f"{BASE_URL}{MOVIES_ENDPOINT}"

        # Отправка запроса на регистрацию
        response = requests.get(movies_url, headers=HEADERS)

        assert response.status_code == 200
        assert response.json()["movies"] is not None
        assert response.json()["count"] is not None
        assert response.json()["page"] is not None
        assert response.json()["pageSize"] is not None
        assert response.json()["pageCount"] is not None
        assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'

    def test_getting_movies_with_params(self):
        # URL для регистрации
        movies_url = f"{BASE_URL}{MOVIES_ENDPOINT}?{PARAMS}"

        # Отправка запроса на регистрацию
        response = requests.get(movies_url, headers=HEADERS)

        assert response.status_code == 200
        assert response.json()["movies"] is not None
        print(len(response.json()["movies"]))
        assert len(response.json()["movies"]) > 0
        assert response.json()["count"] is not None
        assert response.json()["page"] is not None
        assert response.json()["pageSize"] is not None
        assert response.json()["pageCount"] is not None
        assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'