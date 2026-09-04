import requests
import allure
import json


class CourierAPIClient:
    def __init__(self, base_url: str, auth_token: str):
        self.base_url = base_url
        self.auth_token = auth_token
        # НОВОЕ: для Allure-хука
        self._last_request = None
        self._last_response = None

    def _get_auth_header(self):
        if not self.auth_token:
            raise ValueError("AUTH_TOKEN не задан")
        return {"Authorization": f"Bearer {self.auth_token}"}

    # НОВОЕ: централизованный метод для отправки запросов с Allure-вложениями
    def _send_request(self, method, url, headers=None, json_data=None):
        """Отправляет запрос и добавляет вложения в Allure-отчёт."""
        self._last_request = {"url": url, "method": method, "data": json_data}

        # Вложение для запроса
        allure.attach(
            json.dumps({"url": url, "method": method, "body": json_data}, indent=2, ensure_ascii=False),
            name=f"Request: {method} {url}",
            attachment_type=allure.attachment_type.JSON
        )

        response = requests.request(method, url, headers=headers, json=json_data)
        self._last_response = response

        # Вложение для ответа
        try:
            response_data = response.json() if response.text else {}
            allure.attach(
                json.dumps(response_data, indent=2, ensure_ascii=False),
                name=f"Response: {response.status_code}",
                attachment_type=allure.attachment_type.JSON
            )
        except:
            allure.attach(
                response.text or "Empty response",
                name=f"Response: {response.status_code}",
                attachment_type=allure.attachment_type.TEXT
            )

        response.raise_for_status()
        return response

    # ИЗМЕНЕНО: добавлен @allure.step и используется _send_request
    @allure.step("Получение курьера по ID: {courier_id}")
    def get_courier_by_id(self, courier_id: int):
        url = f"{self.base_url}/couriers/{courier_id}"
        headers = self._get_auth_header()
        response = self._send_request("GET", url, headers=headers)
        return response.json()

    # ИЗМЕНЕНО: добавлен @allure.step и используется _send_request
    @allure.step("Создание курьера с данными: {data}")
    def create_courier(self, data: dict):
        url = f"{self.base_url}/couriers"
        headers = self._get_auth_header()
        headers["Content-Type"] = "application/json"
        response = self._send_request("POST", url, headers=headers, json_data=data)
        return response.json()

    # ИЗМЕНЕНО: добавлен @allure.step и используется _send_request
    @allure.step("Обновление курьера с ID: {courier_id}, данные: {data}")
    def update_courier(self, courier_id: int, data: dict):
        url = f"{self.base_url}/couriers/{courier_id}"
        headers = self._get_auth_header()
        headers["Content-Type"] = "application/json"
        response = self._send_request("PATCH", url, headers=headers, json_data=data)
        return response.json()

    # ИЗМЕНЕНО: добавлен @allure.step и используется _send_request
    @allure.step("Удаление курьера с ID: {courier_id}")
    def delete_courier(self, courier_id: int):
        url = f"{self.base_url}/couriers/{courier_id}"
        headers = self._get_auth_header()

        response = self._send_request("DELETE", url, headers=headers)

        return {}
