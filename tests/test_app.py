from app import add

def test_add():
    assert add(2, 3) == 5
import pytest
from app import app  # Импортируем Flask-приложение, чтобы тестировать его


# ----------------------------------------------------------
# ФИКСТУРА ДЛЯ ТЕСТИРОВАНИЯ
# ----------------------------------------------------------
@pytest.fixture()
def client():
    """
    Создаёт тестовый клиент Flask.
    Он позволяет выполнять HTTP-запросы к приложению,
    не поднимая настоящий сервер.
    """
    app.testing = True  # Включаем тестовый режим Flask
    return app.test_client()  # Возвращаем клиент, имитирующий запросы


# ----------------------------------------------------------
# ТЕСТ: Главная HTML-страница
# ----------------------------------------------------------
def test_home_page(client):
    """
    Проверяем, что главная страница (/) отдаёт корректный HTML.
    """
    response = client.get("/")  # Делаем GET-запрос на "/"
    assert response.status_code == 200  # Ожидаем код 200 OK
    assert b"MyApp API" in response.data  # Проверяем, что в HTML есть нужный текст


# ----------------------------------------------------------
# ТЕСТЫ ДЛЯ /api/add
# ----------------------------------------------------------
def test_add_success(client):
    """
    Проверяем успешное сложение: 2 + 3 = 5.
    """
    response = client.get("/api/add?a=2&b=3")  # Отправляем запрос
    data = response.get_json()  # Получаем JSON-ответ
    assert response.status_code == 200  # Проверяем статус
    assert data["result"] == 5  # Проверяем корректность результата


def test_add_invalid_input(client):
    """
    Проверяем, что при передаче нечислового аргумента
    API возвращает ошибку 400.
    """
    response = client.get("/api/add?a=x&b=3")  # Неверный ввод: a = "x"
    assert response.status_code == 400  # Ожидаем ошибку пользователя


# ----------------------------------------------------------
# ТЕСТЫ ДЛЯ /api/multiply
# ----------------------------------------------------------
def test_multiply_success(client):
    """
    Проверяем успешное умножение: 4 * 5 = 20.
    """
    response = client.get("/api/multiply?a=4&b=5")
    data = response.get_json()
    assert response.status_code == 200
    assert data["result"] == 20


def test_multiply_invalid_input(client):
    """
    Проверяем ошибку при передаче неверного значения.
    """
    response = client.get("/api/multiply?a=x&b=5")
    assert response.status_code == 400


# ----------------------------------------------------------
# ТЕСТЫ ДЛЯ /api/divide
# ----------------------------------------------------------
def test_divide_success(client):
    """
    Проверяем успешное деление: 10 / 2 = 5.
    """
    response = client.get("/api/divide?a=10&b=2")
    data = response.get_json()
    assert response.status_code == 200
    assert data["result"] == 5


def test_divide_by_zero(client):
    """
    Проверяем обработку деления на ноль.
    API должен вернуть статус 400, а не падать.
    """
    response = client.get("/api/divide?a=10&b=0")
    assert response.status_code == 400


def test_divide_invalid_input(client):
    """
    Проверяем ошибку при передаче строки в параметр.
    """
    response = client.get("/api/divide?a=10&b=x")
    assert response.status_code == 400
