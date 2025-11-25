from custom_requester.custom_requester import CustomRequester

class UserAPI(CustomRequester):
    BASE_URL = "https://auth.dev-cinescope.coconutqa.ru"
    """
    Класс для работы с API пользователей.
    """

    def __init__(self, session):
        self.session = session
        super().__init__(session, self.BASE_URL)

    def create_user(self, user_data, expected_status=201):
        return self.send_request(
            method="POST",
            endpoint="/user",
            data=user_data,
            expected_status=expected_status
        )

    def get_user(self, user_id, expected_status=200, headers=None):
        return self.send_request(
            method="GET",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status,
            headers=headers
        )

    def delete_user(self, user_id, expected_status=200, headers=None):
        return self.send_request(
            method="DELETE",
            endpoint=f"/user/{user_id}",
            expected_status=expected_status,
            headers=headers
        )

    def clean_up_user(self, user_id):

        # Используем send_request без кастомных headers, чтобы брать текущую сессию
        self.delete_user(user_id)
        self.delete_user(user_id, expected_status=401) # после удаления должно быть 401

