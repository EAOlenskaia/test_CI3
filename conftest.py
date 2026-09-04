import threading
import time
import json
import random
import string
import pytest
import allure
from fake_api import app
from api_client import CourierAPIClient


# --- Существующая фикстура (НЕ МЕНЯЕТСЯ) ---
@pytest.fixture(scope="session")
def fake_server():
    """Запускает fake_api на порту 5001."""
    server_thread = threading.Thread(
        target=app.run,
        kwargs={"port": 5001, "debug": False, "use_reloader": False},
        daemon=True,
    )
    server_thread.start()
    time.sleep(0.5)
    yield


# --- НОВЫЕ фикстуры для изоляции тестов ---

@pytest.fixture(scope="session")
def client(fake_server):
    """Создаёт клиент для API."""
    base_url = "http://127.0.0.1:5001/api"
    token = "test_token_123"
    return CourierAPIClient(base_url, token)


@pytest.fixture
def unique_courier_data():
    """Создаёт уникальные данные для курьера."""
    phone = "+79" + ''.join(random.choices(string.digits, k=9))

    return {
        "first_name": "Иван",
        "last_name": "Петров",
        "phone": phone
    }


@pytest.fixture
def created_courier(client, unique_courier_data):
    """
    Создаёт курьера через API и удаляет его после теста.
    Важно: используется try/finally для гарантированной очистки.
    """
    response = client.create_courier(unique_courier_data)
    courier_id = response["id"]

    yield courier_id, unique_courier_data

    # Очистка после теста — даже если тест упал
    try:
        client.delete_courier(courier_id)
    except Exception as e:
        print(f"Ошибка при удалении курьера {courier_id}: {e}")


# --- НОВЫЙ Allure-хук для автоматических вложений при падении ---

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Allure-хук: при падении теста автоматически прикрепляет
    последний запрос и ответ к отчёту.
    """
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        client = item.funcargs.get("client")
        if client:
            if hasattr(client, "_last_request") and client._last_request:
                allure.attach(
                    json.dumps(client._last_request, indent=2, ensure_ascii=False),
                    name="🔴 Last Request (on failure)",
                    attachment_type=allure.attachment_type.JSON
                )
            if hasattr(client, "_last_response") and client._last_response:
                try:
                    response_data = client._last_response.json() if client._last_response.text else {}
                    allure.attach(
                        json.dumps(response_data, indent=2, ensure_ascii=False),
                        name="🔴 Last Response (on failure)",
                        attachment_type=allure.attachment_type.JSON
                    )
                except:
                    allure.attach(
                        client._last_response.text or "Empty response",
                        name="🔴 Last Response (on failure)",
                        attachment_type=allure.attachment_type.TEXT
                    )
