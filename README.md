# API-тестирование сервиса курьеров

Проект содержит автоматизированные API-тесты для сервиса курьеров с использованием **Pytest**, **Requests**, **Pydantic** и **Allure Report**.

## Используемые технологии

- Python 3.11+
- Pytest
- Requests
- Flask
- Pydantic
- Allure Report

## Структура проекта

.
├── api_client.py          # API-клиент
├── fake_api.py            # Тестовый REST API на Flask
├── models.py              # Pydantic-модели
├── conftest.py            # Фикстуры Pytest
├── test_couriers.py       # API-тесты
├── requirements.txt
├── pytest.ini
└── README.md

## Установка

Создать виртуальное окружение:

python -m venv .venv

Активировать его.

Windows

.venv\Scripts\activate

Linux / macOS

source .venv/bin/activate

Установить зависимости:

pip install -r requirements.txt

## Запуск тестов

Запуск всех тестов:

pytest

или

pytest -v


Запуск с генерацией Allure-отчета:

pytest --alluredir=allure-results

## Просмотр Allure-отчета

После выполнения тестов:

allure serve allure-results

или

allure generate allure-results --clean -o allure-report
allure open allure-report

> Для просмотра отчета должен быть установлен Allure Commandline и Java.

## Что проверяется

### Позитивные сценарии

- создание курьера;
- получение курьера по ID;
- обновление данных курьера;
- удаление курьера.

### Негативные сценарии

- получение несуществующего курьера;
- создание курьера без обязательного поля;
- недоступность сервера (ConnectionError).

## Особенности проекта

- используется отдельный API-клиент (`CourierAPIClient`);
- применяются фикстуры Pytest;
- данные для тестов генерируются автоматически;
- используется Pydantic для валидации ответов API;
- Allure автоматически прикладывает:
  - HTTP-запрос;
  - HTTP-ответ;
  - информацию об ошибке при падении теста.

## Запуск

1. Активировать виртуальное окружение. y
3. Выполнить: pytest --alluredir=allure-results
4. Открыть отчет: allure serve allure-results