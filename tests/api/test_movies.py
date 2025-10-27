import pytest
import requests
from constants import HEADERS, BASE_MOVIE_URL, MOVIES_ENDPOINT, MOVIE_PARAMS

PARAMS = 'pageSize=10&page=1&minPrice=1&maxPrice=1000&locations=SPB&published=true&genreId=1&createdAt=asc'


class TestMoviesAPI:
    def test_getting_movies_no_params(self):
        # URL для регистрации
        movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}"

        # Отправка запроса на регистрацию
        response = requests.get(movies_url, headers=HEADERS)

        assert response.status_code == 200, f'Статус код != 200, а равен {response.status_code}'
        assert response.json()["movies"] is not None
        assert response.json()["count"] is not None
        assert response.json()["page"] is not None
        assert response.json()["pageSize"] is not None
        assert response.json()["pageCount"] is not None
        assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'

    def test_getting_movies_page_size(self):
        # URL для регистрации
        movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}"
        response = requests.get(movies_url, headers=HEADERS)

        assert response.status_code == 200, f'Статус код != 200, а равен {response.status_code}'
        assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'
        assert len(response.json()["movies"]) == 10  # basic == 10
        assert response.json()["pageSize"] == 10  # basic == 10

        movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}?{MOVIE_PARAMS["page_size"]}"

        expected_page_size = ''
        for el in MOVIE_PARAMS["page_size"]:
            if el.isdigit():
                expected_page_size += el
        expected_page_size = int(expected_page_size)

        # Отправка запроса на регистрацию
        response = requests.get(movies_url, headers=HEADERS)

        assert response.status_code == 200, f'Статус код != 200, а равен {response.status_code}'
        assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'
        assert response.json()["movies"] is not None
        assert response.json()["pageSize"] == expected_page_size
        assert len(response.json()["movies"]) == expected_page_size
        assert response.json()["pageCount"] is not None

    def test_getting_movies_page_number(self):
        # URL для регистрации
        movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}"
        response = requests.get(movies_url, headers=HEADERS)

        assert response.status_code == 200, f'Статус код != 200, а равен {response.status_code}'
        assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'
        assert response.json()["page"] == 1  # basic == 1

        movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}?{MOVIE_PARAMS["page"]}"

        expected_page_number = ''
        for el in MOVIE_PARAMS["page"]:
            if el.isdigit():
                expected_page_number += el

        # Отправка запроса на регистрацию
        response = requests.get(movies_url, headers=HEADERS)

        assert response.status_code == 200, f'Статус код != 200, а равен {response.status_code}'
        assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'
        assert response.json()["movies"] is not None
        assert response.json()["pageCount"] is not None
        assert response.json()["page"] == int(expected_page_number)

    def test_getting_movies_filter_by_locations(self):
        # URL для регистрации
        movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}?{MOVIE_PARAMS["location1"]}"
        # Отправка запроса на регистрацию
        response = requests.get(movies_url, headers=HEADERS)

        assert response.json()["movies"] is not None
        assert response.status_code == 200, f'Статус код != 200, ОШИБКА --- {response.json()['error']}, {response.json()["message"]}'
        assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'
        expected_location = MOVIE_PARAMS["location1"][-3:]
        for movie in response.json()["movies"]:
            assert movie["location"] == expected_location

        movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}?{MOVIE_PARAMS["location2"]}"
        # Отправка запроса на регистрацию
        response = requests.get(movies_url, headers=HEADERS)

        assert response.status_code == 200, f'Статус код != 200, а равен {response.status_code}'
        assert response.json()["movies"] is not None
        assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'
        expected_location = MOVIE_PARAMS["location2"][-3:]
        for movie in response.json()["movies"]:
            assert movie["location"] == expected_location

    def test_getting_movies_filter_by_genre_id(self):
        # URL для регистрации
        movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}?{MOVIE_PARAMS["genre_id"]}"

        # Отправка запроса на регистрацию
        response = requests.get(movies_url, headers=HEADERS)
        assert response.status_code == 200, f'Статус код != 200, ОШИБКА --- {response.json()['error']}, {response.json()["message"]}'
        assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'

        expected_genre_id = ''
        for el in MOVIE_PARAMS["genre_id"]:
            if el.isdigit():
                expected_genre_id += el
        expected_genre_id = int(expected_genre_id)

        for movie in response.json()["movies"]:
            assert movie["genreId"] == expected_genre_id
            assert movie["genre"]["name"] == MOVIE_PARAMS['genre_name']



    # def test_getting_movies_filter_by_published(self):
    #     # URL для регистрации
    #     movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}?{MOVIE_PARAMS["published"]}"
    #
    #     # Отправка запроса на регистрацию
    #     response = requests.get(movies_url, headers=HEADERS)
    #
    #     assert response.status_code == 200
    #     assert response.json()["movies"] is not None
    #     print(len(response.json()["movies"]))
    #     assert len(response.json()["movies"]) > 0
    #     assert response.json()["count"] is not None
    #     assert response.json()["page"] is not None
    #     assert response.json()["pageSize"] is not None
    #     assert response.json()["pageCount"] is not None
    #     assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'
    #
    # def test_getting_movies_filter_by_price(self):
    #     # URL для регистрации
    #     movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}?{MOVIE_PARAMS["min_price"]}&{MOVIE_PARAMS["max_price"]}"
    #
    #     # Отправка запроса на регистрацию
    #     response = requests.get(movies_url, headers=HEADERS)
    #     assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'
    #
    #     assert response.json()["movies"] is not None
    #     print(len(response.json()["movies"]))
    #     assert len(response.json()["movies"]) > 0
    #     assert response.json()["count"] is not None
    #     assert response.json()["page"] is not None
    #     assert response.json()["pageSize"] is not None
    #     assert response.json()["pageCount"] is not None
    #
    # def test_getting_movies_filter_by_created_at(self):
    #     # URL для регистрации
    #     movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}?{MOVIE_PARAMS["locations"]}"
    #
    #     # Отправка запроса на регистрацию
    #     response = requests.get(movies_url, headers=HEADERS)
    #
    #     assert response.status_code == 200
    #     assert response.json()["movies"] is not None
    #     print(len(response.json()["movies"]))
    #     assert len(response.json()["movies"]) > 0
    #     assert response.json()["count"] is not None
    #     assert response.json()["page"] is not None
    #     assert response.json()["pageSize"] is not None
    #     assert response.json()["pageCount"] is not None
    #     assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'
    #
    # def test_getting_movies_with_all_params(self):
    #     # URL для регистрации
    #     movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}?{'&'.join(MOVIE_PARAMS.values())}"
    #
    #     # Отправка запроса на регистрацию
    #     response = requests.get(movies_url, headers=HEADERS)
    #
    #     assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'
    #     # assert response.json()["movies"] is not None
    #     # print(len(response.json()["movies"]))
    #     # assert len(response.json()["movies"]) > 0
    #     # assert response.json()["count"] is not None
    #     # assert response.json()["page"] is not None
    #     # assert response.json()["pageSize"] is not None
    #     # assert response.json()["pageCount"] is not None
    #     assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'
