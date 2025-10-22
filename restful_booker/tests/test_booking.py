from restful_booker.tests.constants import BASE_URL


class TestBookings:
    def test_create_booking(self, auth_session, booking_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

    def test_update_booking(self, auth_session, booking_data, modify_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        put_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=modify_data)
        assert put_booking.status_code == 200, "Ошибка при редактировании брони"

        # Проверяем, что измененное бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.json()["firstname"] ==  modify_data["firstname"], "Заданное имя не совпадает с новым значением"
        assert get_booking.json()["lastname"] ==  modify_data["lastname"], "Заданная фамилия не совпадает с новым значением"
        assert get_booking.json()["totalprice"] ==  modify_data["totalprice"], "Стоимость не совпадает с новым значением"
        assert get_booking.json()["depositpaid"] ==  modify_data["depositpaid"], "Заданное значение depositpaid не совпадает с новым"
        assert get_booking.json()["additionalneeds"] ==  modify_data["additionalneeds"], "Заданное значение additionalneeds не совпадает с новым"
        assert get_booking.json()["bookingdates"]['checkin'] ==  modify_data["bookingdates"]['checkin'], "Заданное значение ['bookingdates']['checkin'] не совпадает с новым"
        assert get_booking.json()["bookingdates"]['checkout'] ==  modify_data["bookingdates"]['checkout'], "Заданное значение ['bookingdates']['checkout'] не совпадает с новым"


        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

    def test_patch_booking(self, auth_session, booking_data, modify_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        modify_firstname_lastname = {"firstname": modify_data["firstname"],"lastname": modify_data["lastname"]}
        patch_booking  = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=modify_firstname_lastname)
        assert patch_booking.status_code == 200, "Ошибка при редактировании брони"

        # Проверяем, что измененное бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.json()["firstname"] ==  modify_data["firstname"], "Заданное имя не совпадает с новым значением"
        assert get_booking.json()["lastname"] ==  modify_data["lastname"], "Заданная фамилия не совпадает с новым значением"
        assert get_booking.json()["totalprice"] ==  booking_data["totalprice"], "Стоимость не совпадает с новым значением"
        assert get_booking.json()["depositpaid"] ==  booking_data["depositpaid"], "Заданное значение depositpaid не совпадает с новым"
        assert get_booking.json()["additionalneeds"] ==  booking_data["additionalneeds"], "Заданное значение additionalneeds не совпадает с новым"
        assert get_booking.json()["bookingdates"]['checkin'] ==  booking_data["bookingdates"]['checkin'], "Заданное значение ['bookingdates']['checkin'] не совпадает с новым"
        assert get_booking.json()["bookingdates"]['checkout'] ==  booking_data["bookingdates"]['checkout'], "Заданное значение ['bookingdates']['checkout'] не совпадает с новым"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

    # НЕГАТИВНЫЕ ПРОВЕРКИ
    # ПРОВЕРКИ create_booking
    def test_create_booking_with_empty_body(self, auth_session, error_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=error_data["empty_body"])
        assert create_booking.status_code == 500, "Должна была упасть с кодом ошибки 500 при создании брони"

    def test_create_booking_without_body(self, auth_session, error_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking")
        assert create_booking.status_code == 500, "Должна была упасть с кодом ошибки 500 при создании брони"

    def test_create_booking_with_partial_body(self, auth_session, error_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=error_data["partial_data"])
        assert create_booking.status_code == 500, "Должна была упасть с кодом ошибки 500 при создании брони"

    def test_create_booking_with_empty_fields(self, auth_session, error_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=error_data["empty_fields"])
        assert create_booking.status_code == 200, "Создание не удалось"
        booking_id = create_booking.json().get("bookingid")

        # Проверяем, что измененное бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.json()["firstname"] ==  error_data["empty_fields"]["firstname"], "Заданное имя не совпадает с новым значением"
        assert get_booking.json()["lastname"] ==  error_data["empty_fields"]["lastname"], "Заданная фамилия не совпадает с новым значением"
        assert get_booking.json()["totalprice"] ==  error_data["empty_fields"]["totalprice"], "Стоимость не совпадает с новым значением"
        assert get_booking.json()["depositpaid"] ==  error_data["empty_fields"]["depositpaid"], "Заданное значение depositpaid не совпадает с новым"
        assert get_booking.json()["additionalneeds"] ==  error_data["empty_fields"]["additionalneeds"], "Заданное значение additionalneeds не совпадает с новым"
        # assert get_booking.json()["bookingdates"]['checkin'] ==  error_data["empty_fields"]["bookingdates"]['checkin'], "Заданное значение ['bookingdates']['checkin'] не совпадает с новым"
        # assert get_booking.json()["bookingdates"]['checkout'] ==  error_data["empty_fields"]["bookingdates"]['checkout'], "Заданное значение ['bookingdates']['checkout'] не совпадает с новым"

    def test_create_booking_with_only_unknown_fields(self, auth_session, error_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=error_data["only_unknown_fields"])
        assert create_booking.status_code == 500, "Должна была упасть с кодом ошибки 500 при создании брони"

    def test_create_booking_with_additional_unknown_field(self, auth_session, error_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=error_data["additional_unknown_field"])
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == error_data["additional_unknown_field"]["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == error_data["additional_unknown_field"]["totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == error_data["additional_unknown_field"]["lastname"], "Заданная фамилия не совпадает"
        # Проверяем, что дополнительное поле не существует в полученном бронировании
        print(get_booking.json())
        assert 'additional_field_no_exist' not in get_booking.json(), "Поле 'additional_field_no_exist' должно отсутствовать в ответе."

    # ПРОВЕРКИ get_booking
    def test_get_deleted_booking(self, auth_session, booking_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

        # Проверяем, что бронирование больше недоступно
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "Бронь не удалилась"

    def test_get_non_existent_booking(self, auth_session, booking_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = 0

        # Проверяем, что бронирование нельзя получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 404, "Бронь не найдена"

    # ПРОВЕРКИ delete_booking
    def test_delete_deleted_booking(self, auth_session, booking_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

        # Удаляем удаленное бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code != 201, "Удаление брони удалось"
        assert deleted_booking.status_code == 405, "Удаление брони удалось"

    def test_delete_booking_without_auth(self, no_auth_session, booking_data):
        # Создаём бронирование
        create_booking = no_auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = no_auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        # Удаляем бронирование
        deleted_booking = no_auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 403, "Получен доступ к бронированию, к которому доступа быть не должно"

    def test_delete_non_existent_booking(self, auth_session, booking_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/")
        assert deleted_booking.status_code == 404, "Бронь найдена"

    # ПРОВЕРКИ update_booking
    def test_update_booking_with_empty_body(self, auth_session, booking_data, error_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        put_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=error_data['empty_body'])
        assert put_booking.status_code == 400, "Нет ошибки при редактировании брони"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

    def test_update_booking_without_body(self, auth_session, booking_data, error_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        put_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}")
        assert put_booking.status_code == 400, "Нет ошибки при редактировании брони"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

    def test_update_booking_with_empty_fields(self, auth_session, booking_data, error_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        put_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=error_data['empty_fields'])
        assert put_booking.status_code == 200, "Ошибка при редактировании брони"
        # Проверяем, что измененное бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.json()["firstname"] ==  error_data["empty_fields"]["firstname"], "Заданное имя не совпадает с новым значением"
        assert get_booking.json()["lastname"] ==  error_data["empty_fields"]["lastname"], "Заданная фамилия не совпадает с новым значением"
        assert get_booking.json()["totalprice"] ==  error_data["empty_fields"]["totalprice"], "Стоимость не совпадает с новым значением"
        assert get_booking.json()["depositpaid"] ==  error_data["empty_fields"]["depositpaid"], "Заданное значение depositpaid не совпадает с новым"
        assert get_booking.json()["additionalneeds"] ==  error_data["empty_fields"]["additionalneeds"], "Заданное значение additionalneeds не совпадает с новым"
        # assert get_booking.json()["bookingdates"]['checkin'] ==  error_data["empty_fields"]["bookingdates"]['checkin'], "Заданное значение ['bookingdates']['checkin'] не совпадает с новым"
        # assert get_booking.json()["bookingdates"]['checkout'] ==  error_data["empty_fields"]["bookingdates"]['checkout'], "Заданное значение ['bookingdates']['checkout'] не совпадает с новым"


        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

    def test_update_booking_with_partial_data(self, auth_session, booking_data, error_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"


        put_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=error_data['partial_data'])
        assert put_booking.status_code == 400, "Нет ошибки при редактировании брони"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

    def test_update_booking_with_only_unknown_fields(self, auth_session, booking_data, error_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        put_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=error_data['only_unknown_fields'])
        assert put_booking.status_code == 400, "Нет ошибки при редактировании брони"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

    def test_update_booking_with_additional_unknown_field(self, auth_session, booking_data, error_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        put_booking = auth_session.put(f"{BASE_URL}/booking/{booking_id}", json=error_data['additional_unknown_field'])
        assert put_booking.status_code == 200, "Нет ошибки при редактировании брони"
        # Проверяем, что измененное бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.json()["firstname"] == error_data['additional_unknown_field']["firstname"], "Заданное имя не совпадает с новым значением"
        assert get_booking.json()["lastname"] == error_data['additional_unknown_field']["lastname"], "Заданная фамилия не совпадает с новым значением"
        assert get_booking.json()["totalprice"] == error_data['additional_unknown_field']["totalprice"], "Стоимость не совпадает с новым значением"
        assert get_booking.json()["depositpaid"] == error_data['additional_unknown_field']["depositpaid"], "Заданное значение depositpaid не совпадает с новым"
        assert get_booking.json()["additionalneeds"] == error_data['additional_unknown_field']["additionalneeds"], "Заданное значение additionalneeds не совпадает с новым"
        assert get_booking.json()["bookingdates"]['checkin'] == error_data['additional_unknown_field']["bookingdates"]['checkin'], "Заданное значение ['bookingdates']['checkin'] не совпадает с новым"
        assert get_booking.json()["bookingdates"]['checkout'] == error_data['additional_unknown_field']["bookingdates"]['checkout'], "Заданное значение ['bookingdates']['checkout'] не совпадает с новым"

        assert 'additional_field_no_exist' not in get_booking.json(), "Поле 'additional_field_no_exist' должно отсутствовать в ответе."

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

    # ПРОВЕРКИ patch_booking
    def test_patch_booking_with_empty_body(self, auth_session, booking_data, error_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        patch_booking  = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=error_data['empty_body'])
        assert patch_booking.status_code == 200, "Ошибка при редактировании брони"

        # Проверяем, что измененное бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.json()["firstname"] ==  booking_data["firstname"], "Заданное имя не совпадает с новым значением"
        assert get_booking.json()["lastname"] ==  booking_data["lastname"], "Заданная фамилия не совпадает с новым значением"
        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

    def test_patch_booking_with_empty_fields(self, auth_session, booking_data, error_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        modify_firstname_lastname = {"firstname": error_data['empty_fields']["firstname"],"lastname":  error_data['empty_fields']["lastname"]}
        patch_booking  = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=modify_firstname_lastname)
        assert patch_booking.status_code == 200, "Ошибка при редактировании брони"

        # Проверяем, что измененное бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.json()["firstname"] ==  error_data['empty_fields']["firstname"], "Заданное имя не совпадает с новым значением"
        assert get_booking.json()["lastname"] ==  error_data['empty_fields']["lastname"], "Заданная фамилия не совпадает с новым значением"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

    def test_patch_booking_without_body(self, auth_session, booking_data, error_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        patch_booking  = auth_session.patch(f"{BASE_URL}/booking/{booking_id}")
        assert patch_booking.status_code == 200, "Ошибка при редактировании брони"

        # Проверяем, что измененное бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.json()["firstname"] ==  booking_data["firstname"], "Заданное имя не совпадает с новым значением"
        assert get_booking.json()["lastname"] ==  booking_data["lastname"], "Заданная фамилия не совпадает с новым значением"
        assert get_booking.json()["totalprice"] ==  booking_data["totalprice"], "Стоимость не совпадает с новым значением"
        assert get_booking.json()["depositpaid"] ==  booking_data["depositpaid"], "Заданное значение depositpaid не совпадает с новым"
        assert get_booking.json()["additionalneeds"] ==  booking_data["additionalneeds"], "Заданное значение additionalneeds не совпадает с новым"
        assert get_booking.json()["bookingdates"]['checkin'] ==  booking_data["bookingdates"]['checkin'], "Заданное значение ['bookingdates']['checkin'] не совпадает с новым"
        assert get_booking.json()["bookingdates"]['checkout'] ==  booking_data["bookingdates"]['checkout'], "Заданное значение ['bookingdates']['checkout'] не совпадает с новым"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"

    def test_patch_booking_with_additional_unknown_field(self, auth_session, booking_data, error_data):
        # Создаём бронирование
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200, "Ошибка при создании брони"

        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "Идентификатор брони не найден в ответе"
        assert create_booking.json()["booking"]["firstname"] == booking_data["firstname"], "Заданное имя не совпадает"
        assert create_booking.json()["booking"]["totalprice"] == booking_data[
            "totalprice"], "Заданная стоимость не совпадает"

        # Проверяем, что бронирование можно получить по ID
        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200, "Бронь не найдена"
        assert get_booking.json()["lastname"] == booking_data["lastname"], "Заданная фамилия не совпадает"

        patch_booking  = auth_session.patch(f"{BASE_URL}/booking/{booking_id}", json=error_data["additional_unknown_field"]['additional_field_no_exist'])
        assert patch_booking.status_code == 400, "Ошибка при редактировании брони"

        # Удаляем бронирование
        deleted_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert deleted_booking.status_code == 201, "Бронь не удалилась"











