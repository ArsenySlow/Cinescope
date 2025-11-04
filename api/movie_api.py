from urllib.parse import urlencode
from custom_requester.custom_requester import CustomRequester
from constants import BASE_MOVIE_URL

class MovieAPI(CustomRequester):
    """
    Класс для работы с API пользователей.
    """

    def __init__(self, session):
        super().__init__(session = session, base_url=BASE_MOVIE_URL)
        self.session = session

    @staticmethod
    def build_query_string(params: dict) -> str:
        """
        Преобразует словарь параметров в query-строку формата '?key=value&key2=value2'.
        - игнорирует None и пустые значения
        - списки (например locations) объединяет через запятую
        """
        if not params:
            return ""

        filtered = {}
        for key, value in params.items():
            if value is None or value == "":
                continue
            if isinstance(value, list):
                filtered[key] = ",".join(map(str, value))
            else:
                filtered[key] = str(value)

        query_string = "?" + urlencode(filtered)
        return query_string

    def get_movies_info(
            self,
            expected_status: int = 200,
            headers: dict = None,
            params: dict = None,
    ):
        """
        Получение списка фильмов. Если переданы params — они будут добавлены в URL как query-параметры.
        """
        query_string = self.build_query_string(params)
        endpoint = f"/movies{query_string}"

        return self.send_request(
            method="GET",
            endpoint=endpoint,
            expected_status=expected_status,
            headers=headers
        )

    def delete_movie(self, movie_id, expected_status=200, headers=None):
        return self.send_request(
            method="DELETE",
            endpoint=f"/movie/{movie_id}",
            expected_status=expected_status,
            headers=headers
        )

    # def get_movies_info(self, movie_id, expected_status=200, headers=None):
    #     return self.send_request(
    #         method="GET",
    #         endpoint=f"/movies/{movie_id}",
    #         expected_status=expected_status,
    #         headers=headers
    #     )

    def delete_movie(self, movie_id, expected_status=200, headers=None):
        return self.send_request(
            method="DELETE",
            endpoint=f"/movie/{movie_id}",
            expected_status=expected_status,
            headers=headers
        )