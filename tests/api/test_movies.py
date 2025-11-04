from api.api_manager import ApiManager

class TestMoviesAPI:

    def test_getting_movies_no_params(self, api_manager: ApiManager, test_user):
        # Получение списка фильмов без параметров
        response = api_manager.movie_api.get_movies_info()
        response_data = response.json()

        # Проверка отсутствия ошибок
        assert response.status_code == 200, f"Неверный статус ответа: {response.status_code}, тело: {response.text}"
        assert "error" not in response_data, f"Ошибка в ответе: {response_data.get('error')}, сообщение: {response_data.get('message')}"

        # Проверка структуры ответа
        assert "movies" in response_data, "В ответе отсутствует ключ 'movies'"
        assert response_data["movies"] is not None, "Поле 'movies' пустое"

        assert "count" in response_data, "В ответе отсутствует ключ 'count'"
        assert response_data["count"] is not None, "Поле 'count' пустое"

        assert "page" in response_data, "В ответе отсутствует ключ 'page'"
        assert response_data["page"] is not None, "Поле 'page' пустое"

        assert "pageSize" in response_data, "В ответе отсутствует ключ 'pageSize'"
        assert response_data["pageSize"] is not None, "Поле 'pageSize' пустое"

        assert "pageCount" in response_data, "В ответе отсутствует ключ 'pageCount'"
        assert response_data["pageCount"] is not None, "Поле 'pageCount' пустое"

        # Проверка структуры основного ответа
        for key in ["movies", "count", "page", "pageSize", "pageCount"]:
            assert key in response_data, f"В ответе отсутствует ключ '{key}'"
            assert response_data[key] is not None, f"Поле '{key}' пустое"

        # Проверка структуры всех фильмов
        movies = response_data["movies"]
        assert isinstance(movies, list), "Поле 'movies' должно быть списком"

        for i, movie in enumerate(movies):
            assert "name" in movie["genre"], f"У фильма c айди #{movies[i]["id"]} отсутствует имя жанра ('genre.name')"
            for field in [
                "id", "name", "price", "description", "imageUrl",
                "location", "published", "genreId", "genre", "createdAt", "rating"
            ]:
                assert field in movie, f"У фильма #{i} отсутствует поле '{field}'"


    def test_getting_movies_with_filters(self, api_manager: ApiManager):
        """Проверка получения фильмов с фильтрами"""
        params = {
            "pageSize": 5,
            "page": 2,
            "minPrice": 100,
            "maxPrice": 500,
            "locations": ["MSK", "SPB"],
            "published": True,
            "genreId": 1,
            "createdAt": "desc",
        }

        response = api_manager.movie_api.get_movies_info(params=params)
        data = response.json()

        # Базовые проверки
        assert response.status_code == 200, f"Неверный статус: {response.status_code}, тело: {response.text}"
        assert "error" not in data, f"Ошибка в ответе: {data.get('error')}, сообщение: {data.get('message')}"

        # Проверка структуры ответа
        assert "movies" in data, "Ответ не содержит ключ 'movies'"
        assert isinstance(data["movies"], list), "Поле 'movies' должно быть списком"
        assert "count" in data, "Нет поля 'count'"
        assert "page" in data, "Нет поля 'page'"
        assert "pageSize" in data, "Нет поля 'pageSize'"
        assert "pageCount" in data, "Нет поля 'pageCount'"

        # Проверка фильмов
        if data["movies"]:
            movie = data["movies"][0]
            for field in ["id", "name", "price", "description", "imageUrl", "location",
                          "published", "genreId", "genre", "createdAt", "rating"]:
                assert field in movie, f"В фильме отсутствует поле '{field}'"
            assert params["minPrice"] <= movie["price"] <= params["maxPrice"], "Цена вне указанного диапазона"
            assert movie["location"] in params["locations"], "Локация не соответствует фильтру"
            assert movie["published"] == params["published"], "Флаг 'published' не соответствует фильтру"
            assert movie["genreId"] == params["genreId"], "Жанр не соответствует фильтру"


    # def test_getting_movies_page_size(self):
    #     # URL для регистрации
    #     movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}"
    #     response = requests.get(movies_url, headers=HEADERS)
    #
    #     assert response.status_code == 200, f'Статус код != 200, а равен {response.status_code}'
    #     assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'
    #     assert len(response.json()["movies"]) == 10  # basic == 10
    #     assert response.json()["pageSize"] == 10  # basic == 10
    #
    #     movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}?{MOVIE_PARAMS["page_size"]}"
    #
    #     expected_page_size = ''
    #     for el in MOVIE_PARAMS["page_size"]:
    #         if el.isdigit():
    #             expected_page_size += el
    #     expected_page_size = int(expected_page_size)
    #
    #     # Отправка запроса на регистрацию
    #     response = requests.get(movies_url, headers=HEADERS)
    #
    #     assert response.status_code == 200, f'Статус код != 200, а равен {response.status_code}'
    #     assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'
    #     assert response.json()["movies"] is not None
    #     assert response.json()["pageSize"] == expected_page_size
    #     assert len(response.json()["movies"]) == expected_page_size
    #     assert response.json()["pageCount"] is not None
    #
    # def test_getting_movies_page_number(self):
    #     # URL для регистрации
    #     movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}"
    #     response = requests.get(movies_url, headers=HEADERS)
    #
    #     assert response.status_code == 200, f'Статус код != 200, а равен {response.status_code}'
    #     assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'
    #     assert response.json()["page"] == 1  # basic == 1
    #
    #     movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}?{MOVIE_PARAMS["page"]}"
    #
    #     expected_page_number = ''
    #     for el in MOVIE_PARAMS["page"]:
    #         if el.isdigit():
    #             expected_page_number += el
    #
    #     # Отправка запроса на регистрацию
    #     response = requests.get(movies_url, headers=HEADERS)
    #
    #     assert response.status_code == 200, f'Статус код != 200, а равен {response.status_code}'
    #     assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'
    #     assert response.json()["movies"] is not None
    #     assert response.json()["pageCount"] is not None
    #     assert response.json()["page"] == int(expected_page_number)
    #
    # def test_getting_movies_filter_by_locations(self):
    #     # URL для регистрации
    #     movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}?{MOVIE_PARAMS["location1"]}"
    #     # Отправка запроса на регистрацию
    #     response = requests.get(movies_url, headers=HEADERS)
    #
    #     assert response.json()["movies"] is not None
    #     assert response.status_code == 200, f'Статус код != 200, ОШИБКА --- {response.json()['error']}, {response.json()["message"]}'
    #     assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'
    #     expected_location = MOVIE_PARAMS["location1"][-3:]
    #     for movie in response.json()["movies"]:
    #         assert movie["location"] == expected_location
    #
    #     movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}?{MOVIE_PARAMS["location2"]}"
    #     # Отправка запроса на регистрацию
    #     response = requests.get(movies_url, headers=HEADERS)
    #
    #     assert response.status_code == 200, f'Статус код != 200, а равен {response.status_code}'
    #     assert response.json()["movies"] is not None
    #     assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'
    #     expected_location = MOVIE_PARAMS["location2"][-3:]
    #     for movie in response.json()["movies"]:
    #         assert movie["location"] == expected_location
    #
    # def test_getting_movies_filter_by_genre_id(self):
    #     # URL для регистрации
    #     movies_url = f"{BASE_MOVIE_URL}{MOVIES_ENDPOINT}?{MOVIE_PARAMS["genre_id"]}"
    #
    #     # Отправка запроса на регистрацию
    #     response = requests.get(movies_url, headers=HEADERS)
    #     assert response.status_code == 200, f'Статус код != 200, ОШИБКА --- {response.json()['error']}, {response.json()["message"]}'
    #     assert "error" not in response.json(), f' Ошибка - {response.json()["error"]}, {response.json()["message"]}'
    #
    #     expected_genre_id = ''
    #     for el in MOVIE_PARAMS["genre_id"]:
    #         if el.isdigit():
    #             expected_genre_id += el
    #     expected_genre_id = int(expected_genre_id)
    #
    #     for movie in response.json()["movies"]:
    #         assert movie["genreId"] == expected_genre_id
    #         assert movie["genre"]["name"] == MOVIE_PARAMS['genre_name']













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
