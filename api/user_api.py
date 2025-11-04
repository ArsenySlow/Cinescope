from custom_requester.custom_requester import CustomRequester
from constants import BASE_URL

class UserAPI(CustomRequester):
    """
    Класс для работы с API пользователей.
    """

    def __init__(self, session):
        super().__init__(session = session, base_url=BASE_URL)
        self.session = session

    def get_user_info(self, user_id, expected_status=200, headers=None):
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

