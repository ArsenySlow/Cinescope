from constants.constants import BASE_MOVIE_FIELDS, PARAMS
import pytest


class TestMoviesAPI:

    @staticmethod
    def validate_movie_structure(movie: dict):
        """Проверка структуры одной записи фильма"""
        for field in BASE_MOVIE_FIELDS:
            assert field in movie, f"Нет обязательного поля '{field}' в фильме: {movie}"

        assert isinstance(movie["genre"], dict), "Поле 'genre' должно быть объектом"
        assert "name" in movie["genre"], "Нет поля genre.name"

    def test_getting_movies_no_params(self, super_admin):
        response = super_admin.api.movie_api.get_movies_info()
        assert response.status_code == 200, f"Ошибка статус: {response.status_code}, тело: {response.text}"

        data = response.json()
        assert data.get("error") is None, f"Ошибка API: {data}"

        # Проверка ключей корневого объекта
        for key in ["movies", "count", "page", "pageSize", "pageCount"]:
            assert key in data, f"Нет ключа '{key}' в ответе"

        assert isinstance(data["movies"], list), "movies должен быть списком"

        # Проверка каждого фильма
        for movie in data["movies"]:
            self.validate_movie_structure(movie)

    @pytest.mark.parametrize(
        "case_name, params",
        [
            ("no_filters", {}),  # без фильтров
            ("all_filters", PARAMS),  # все фильтры сразу
            ("minPrice", {"minPrice": PARAMS["minPrice"]}),
            ("maxPrice", {"maxPrice": PARAMS["maxPrice"]}),
            ("locations", {"locations": PARAMS["locations"]}),
            ("published", {"published": PARAMS["published"]}),
            ("genreId", {"genreId": PARAMS["genreId"]}),
            ("pageSize", {"pageSize": PARAMS["pageSize"]}),
            ("page", {"page": PARAMS["page"]}),
            ("createdAt", {"createdAt": PARAMS["createdAt"]}),
        ],
        ids=[
            "no_filters",
            "all_filters",
            "minPrice",
            "maxPrice",
            "locations",
            "published",
            "genreId",
            "pageSize",
            "page",
            "createdAt",
        ]
    )
    def test_getting_movies_with_filters(self, case_name, params, super_admin):
        response = super_admin.api.movie_api.get_movies_info(params=params)
        assert response.status_code == 200

        data = response.json()
        assert data.get("error") is None

        movies = data["movies"]
        assert isinstance(movies, list)

        for movie in movies:
            self.validate_movie_structure(movie)

            # --- проверки фильтров ---
            if not params:
                continue  # кейс без фильтров

            # кейс "все фильтры"
            if case_name == "all_filters":
                assert movie["price"] >= params["minPrice"]
                assert movie["price"] <= params["maxPrice"]
                assert movie["location"] in params["locations"]
                assert movie["published"] == params["published"]
                assert movie["genreId"] == params["genreId"]
                assert len(movies) <= params["pageSize"]
                assert data["page"] == params["page"]
                assert params["createdAt"] in ["asc", "desc"]
                continue

            # частичный фильтр (по одному)
            filter_name, filter_value = list(params.items())[0]

            match filter_name:
                case "minPrice":
                    assert movie["price"] >= filter_value
                case "maxPrice":
                    assert movie["price"] <= filter_value
                case "locations":
                    assert movie["location"] in filter_value
                case "published":
                    assert movie["published"] == filter_value
                case "genreId":
                    assert movie["genreId"] == filter_value
                case "pageSize":
                    assert len(movies) <= filter_value
                case "page":
                    assert data["page"] == filter_value
                case "createdAt":
                    assert filter_value in ["asc", "desc"]

    @pytest.mark.slow
    def test_create_movie(self, super_admin, created_movie, movie_data):
        """Создание фильма под админом"""

        movie = created_movie

        # Проверки структуры
        for field in ["id", "name", "price", "description", "location",
                      "published", "genreId", "genre", "createdAt", "rating"]:
            assert field in movie, f"Отсутствует поле '{field}'"

        # Проверки на совпадение отправленных данных
        assert movie["name"] == movie_data["name"]
        assert movie["price"] == movie_data["price"]
        assert movie["location"] == movie_data["location"]
        assert movie["description"] == movie_data["description"]
        assert movie["published"] == movie_data["published"]
        assert movie["genreId"] == movie_data["genreId"]

        # Проверка: можно получить фильм по ID и данные совпадут
        response_get = super_admin.api.movie_api.get_movie_by_id(movie["id"])
        assert response_get.status_code == 200
        movie_get = response_get.json()
        for key in ["id", "name", "price", "description", "location",
                    "published", "genreId"]:
            assert movie_get[key] == movie[key], f"Несовпадение поля '{key}' при GET по ID"

    def test_create_movie_invalid_data(self, super_admin):
        """POST /movies с некорректными данными должен вернуть 400"""
        invalid_data = {}
        super_admin.api.movie_api.create_movie(invalid_data, expected_status=400)

    def test_get_movie_by_id(self, super_admin, created_movie, movie_data):
        """Создание фильма под админом"""

        movie = created_movie

        # Проверка: можно получить фильм по ID и данные совпадут
        response_get = super_admin.api.movie_api.get_movie_by_id(movie["id"])
        assert response_get.status_code == 200
        movie_get = response_get.json()
        for key in ["id", "name", "price", "description", "location",
                    "published", "genreId"]:
            assert movie_get[key] == movie[key], f"Несовпадение поля '{key}' при GET по ID"

    def test_get_movie_by_nonexistent_id(self, super_admin):
        """GET /movies/{id} с несуществующим ID должен вернуть 404"""
        non_existing_id = 999999999999
        super_admin.api.movie_api.get_movie_by_id(non_existing_id, expected_status=500)

    def test_update_movie_invalid_data(self, super_admin, created_movie):
        """PATCH /movies/{id} с некорректными данными должен вернуть 400"""
        movie = created_movie
        invalid_update = {
            "price": -500,  # некорректная цена
            "published": "not_boolean"  # некорректный тип
        }

        response = super_admin.api.movie_api.update_movie(
            movie_id=movie["id"],
            data=invalid_update,
            expected_status=400
        )
        assert response.status_code == 400, f"Ожидался 400, получен {response.status_code}, тело: {response.text}"
        data = response.json()
        assert "error" in data or "message" in data, f"Ошибка не описана в ответе: {data}"

    def test_update_movie(self, super_admin, created_movie, updated_movie_data):
        """
        Редактирование фильма
        """
        movie = created_movie

        # PATCH
        response = super_admin.api.movie_api.update_movie(movie_id=movie["id"], data=updated_movie_data)
        assert response.status_code == 200, response.text

        updated_movie = response.json()

        # Проверка структуры
        for field in ["id", "name", "price", "description", "location",
                      "published", "genreId", "genre", "createdAt", "rating", "imageUrl"]:
            assert field in updated_movie, f"Отсутствует поле '{field}'"

        # Проверка соответствия обновленных данных
        for key in updated_movie_data:
            assert updated_movie[key] == updated_movie_data[key], f"Несовпадение поля '{key}' после обновления"

        # GET по ID, проверка что данные сохранились
        response_get = super_admin.api.movie_api.get_movie_by_id(movie["id"])
        assert response_get.status_code == 200
        movie_get = response_get.json()
        for key in updated_movie_data:
            assert movie_get[key] == updated_movie[key], f"GET по ID: Несовпадение поля '{key}' после обновления"

    @pytest.mark.slow
    @pytest.mark.parametrize(
        "user_fixture, expected_status",
        [
            ("super_admin", 200),
            ("admin", 403),
            ("common_user", 403),
        ],
        ids=["super_admin_can_delete", "admin_forbidden", "user_forbidden"]
    )
    def test_delete_movie(self, user_fixture, expected_status, super_admin, movie_data, request):
        # Берём объект фикстуры по имени
        user = request.getfixturevalue(user_fixture)

        response = super_admin.api.movie_api.create_movie(movie_data)
        movie = response.json()

        user.api.movie_api.delete_movie(movie["id"],expected_status)

        if expected_status == 200:
            response_get = super_admin.api.movie_api.get_movie_by_id(movie["id"], expected_status=404)
            data = response_get.json()
            assert data["error"] == "Not Found"

    @pytest.mark.slow
    def test_create_movie_by_user(self, common_user):
        common_user.api.movie_api.create_movie(data=None, expected_status=403)
