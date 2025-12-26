"""
backend/tests/test_app.py

Тесты для Flask backend API.

ВАЖНОЕ:
- Раньше API мог возвращать плоский формат:
    {"result": 5}
- Сейчас мы используем единый формат ответа (правильный для API):
    {
      "success": true,
      "data": { "result": 5, ... },
      "error": null
    }

Из-за этого старые тесты падали с:
  KeyError: 'result'
потому что result теперь лежит внутри data.
"""

import pytest

# =========================================================
# 1) Фикстура client
# ---------------------------------------------------------
# Flask предоставляет test_client(), через который мы можем
# делать запросы к API БЕЗ запуска сервера.
#
# То есть:
# - не нужен localhost
# - не нужен Render
# - тесты работают чисто внутри Python процесса
# =========================================================
@pytest.fixture
def client():
    """
    Создает тестовый клиент Flask для выполнения запросов.
    """
    # Импортируем Flask app из backend/app.py
    # ВАЖНО: в app.py должен быть объект app = Flask(__name__)
    from app import app

    # Включаем тестовый режим Flask (удобно для ошибок и тестов)
    app.config["TESTING"] = True

    # Создаем клиента
    with app.test_client() as client:
        yield client


# =========================================================
# 2) Вспомогательные функции (чтобы тесты были понятнее)
# =========================================================
def assert_success_response(response):
    """
    Проверяет, что ответ:
    - HTTP 200
    - JSON содержит success=True
    - error=None
    - data существует и это dict
    Возвращает распарсенный json, чтобы дальше проверять data.
    """
    assert response.status_code == 200

    payload = response.get_json()
    assert payload is not None, "Ответ не является JSON"

    # Проверяем "контейнер" ответа
    assert payload.get("success") is True
    assert payload.get("error") is None
    assert isinstance(payload.get("data"), dict)

    return payload


def assert_has_result(payload, expected):
    """
    Проверяет, что payload["data"]["result"] существует и равен expected.
    """
    assert "result" in payload["data"], "В data нет ключа 'result'"
    assert payload["data"]["result"] == expected


# =========================================================
# 3) Тесты эндпоинтов калькулятора
# =========================================================
def test_add(client):
    """
    Проверяет эндпоинт /api/add
    Пример: /api/add?a=2&b=3 -> result=5
    """
    response = client.get("/api/add?a=2&b=3")

    payload = assert_success_response(response)
    assert_has_result(payload, 5.0)


def test_multiply(client):
    """
    Проверяет эндпоинт /api/multiply
    Пример: /api/multiply?a=4&b=5 -> result=20
    """
    response = client.get("/api/multiply?a=4&b=5")

    payload = assert_success_response(response)
    assert_has_result(payload, 20.0)


def test_divide(client):
    """
    Проверяет эндпоинт /api/divide
    Пример: /api/divide?a=10&b=2 -> result=5
    """
    response = client.get("/api/divide?a=10&b=2")

    payload = assert_success_response(response)
    assert_has_result(payload, 5.0)


def test_health(client):
    """
    Healthcheck тест:
    Render использует /health, мы проверяем что он живой.
    Тут формат простой: {"status":"ok"}
    """
    response = client.get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
