"""
app.py — Flask backend (middle-level version)
============================================

Этот модуль реализует API-сервис с несколькими эндпоинтами, структурой проекта,
обработкой ошибок и логированием. Подходит как демонстрационный backend
для CI/CD, Docker, Render, GitHub Actions, тестирования и интеграции с React.
"""

from flask import Flask, jsonify, request, Blueprint
import logging


# -----------------------------------------------------------------------------
# Создаем Flask-приложение
# -----------------------------------------------------------------------------
app = Flask(__name__)

# Включаем логирование в формате INFO (доступно в Render logs)
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Blueprint — профессиональная структура API
# -----------------------------------------------------------------------------
api = Blueprint("api", __name__, url_prefix="/api")


# -----------------------------------------------------------------------------
# Вспомогательная функция безопасного преобразования параметра в число
# -----------------------------------------------------------------------------
def parse_number(value):
    """
    Преобразует строковое значение в float.
    Если значение некорректно — возвращает None.
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return None


# -----------------------------------------------------------------------------
# /api/add — сложение
# -----------------------------------------------------------------------------
@api.get("/add")
def add():
    """
    Складывает два числа, полученных через параметры запроса:
       /api/add?a=2&b=3
    """
    a = parse_number(request.args.get("a"))
    b = parse_number(request.args.get("b"))

    if a is None or b is None:
        return jsonify(error="Invalid input, numbers expected"), 400

    result = a + b
    logger.info(f"ADD: {a} + {b} = {result}")
    return jsonify(result=result)


# -----------------------------------------------------------------------------
# /api/multiply — умножение
# -----------------------------------------------------------------------------
@api.get("/multiply")
def multiply():
    """
    Умножает два числа:
       /api/multiply?a=4&b=5
    """
    a = parse_number(request.args.get("a"))
    b = parse_number(request.args.get("b"))

    if a is None or b is None:
        return jsonify(error="Invalid input, numbers expected"), 400

    result = a * b
    logger.info(f"MULTIPLY: {a} * {b} = {result}")
    return jsonify(result=result)


# -----------------------------------------------------------------------------
# /api/divide — деление (с обработкой деления на ноль)
# -----------------------------------------------------------------------------
@api.get("/divide")
def divide():
    """
    Делит число a на b с проверкой деления на 0:
       /api/divide?a=10&b=2
    """
    a = parse_number(request.args.get("a"))
    b = parse_number(request.args.get("b"))

    if a is None or b is None:
        return jsonify(error="Invalid input, numbers expected"), 400

    if b == 0:
        return jsonify(error="Division by zero is not allowed"), 400

    result = a / b
    logger.info(f"DIVIDE: {a} / {b} = {result}")
    return jsonify(result=result)


# -----------------------------------------------------------------------------
# Healthcheck — для Render/Kubernetes
# -----------------------------------------------------------------------------
@app.get("/health")
def health_check():
    """
    Простой healthcheck для мониторинга.
    Используется Render, Docker и CI, чтобы понять, что приложение живо.
    """
    return jsonify(status="ok")


# -----------------------------------------------------------------------------
# Главная страница — HTML заглушка (используется для проверки деплоя)
# -----------------------------------------------------------------------------
@app.get("/")
def home():
    """
    Возвращает простую HTML-страницу.
    Eё удобно проверять в браузере после деплоя.
    """
    return """
    <html>
        <head><title>MyApp API</title></head>
        <body>
            <h1>MyApp API Backend (Flask)</h1>
            <p>Status: running</p>
            <p>Try endpoints:</p>
            <ul>
                <li>/api/add?a=2&b=3</li>
                <li>/api/multiply?a=4&b=5</li>
                <li>/api/divide?a=10&b=2</li>
                <li>/health</li>
            </ul>
        </body>
    </html>
    """


# -----------------------------------------------------------------------------
# Регистрируем Blueprint API
# -----------------------------------------------------------------------------
app.register_blueprint(api)


# -----------------------------------------------------------------------------
# Точка входа (если запускать локально: python app.py)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    # Приложение слушает порт 10000 (Render использует EXPOSE 10000)
    logger.info("Starting Flask development server on port 10000 ...")
    app.run(host="0.0.0.0", port=10000)
