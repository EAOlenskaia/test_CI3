import pytest
import requests
import allure
from models import CourierModel
from api_client import CourierAPIClient

import pytest
import requests
import allure

from api_client import CourierAPIClient
from models import CourierModel


@allure.feature("Курьеры")
class TestCourierClient:

    @allure.story("Создание курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_courier(self, client, unique_courier_data):

        with allure.step("Создание курьера"):
            response = client.create_courier(unique_courier_data)

        with allure.step("Проверка ответа"):
            courier = CourierModel(**response)

            assert courier.id > 0
            assert courier.first_name == unique_courier_data["first_name"]
            assert courier.last_name == unique_courier_data["last_name"]
            assert courier.phone == unique_courier_data["phone"]

    @allure.story("Получение курьера")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_courier_by_id(self, client, created_courier):

        courier_id, data = created_courier

        with allure.step("Получение курьера"):
            response = client.get_courier_by_id(courier_id)

        courier = CourierModel(**response)

        assert courier.id == courier_id
        assert courier.first_name == data["first_name"]
        assert courier.last_name == data["last_name"]
        assert courier.phone == data["phone"]

    @allure.story("Обновление курьера")
    @allure.severity(allure.severity_level.NORMAL)
    def test_update_courier(self, client, created_courier):

        courier_id, _ = created_courier

        new_last_name = "Иванов"

        updated = client.update_courier(
            courier_id,
            {
                "last_name": new_last_name
            }
        )

        courier = CourierModel(**updated)

        assert courier.id == courier_id
        assert courier.last_name == new_last_name

    @allure.story("Удаление курьера")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_courier(self, client, created_courier):

        courier_id, _ = created_courier

        client.delete_courier(courier_id)

        with pytest.raises(requests.exceptions.HTTPError):
            client.get_courier_by_id(courier_id)

    @allure.story("Негативные сценарии")
    @allure.severity(allure.severity_level.MINOR)
    def test_connection_error(self):

        invalid_client = CourierAPIClient(
            "http://invalid-url:9999",
            "token"
        )

        with pytest.raises(requests.exceptions.ConnectionError):
            invalid_client.get_courier_by_id(1)

    @allure.story("Негативные сценарии")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_nonexistent_courier(self, client):

        with pytest.raises(requests.exceptions.HTTPError, match="404"):
            client.get_courier_by_id(99999)

    @allure.story("Негативные сценарии")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_courier_without_required_field(self, client):

        with pytest.raises(requests.exceptions.HTTPError) as exc:

            client.create_courier(
                {
                    "phone": "+79999999999"
                }
            )

        assert exc.value.response.status_code == 400