"""
backend/app.py

Основной файл backend-приложения.
Flask API + CORS + базовая бизнес-логика (калькулятор).
"""

from flask import Flask, request, jsonify
from flask_cors import CORS

# ============================================================
# 1. Инициализация Flask-приложения
# ============================================================

app = Flask(__name__)

# ------------------------------------------------------------
# Включаем CORS
# ------------------------------------------------------------
# Это КРИТИЧЕСКИ важно для frontend (React),
# т.к. frontend и backend находятся на разных доменах:
# - frontend: http://localhost:3000
# - backend:  https://*.onrender.com
#
# resources={r"/api/*": {"origins": "*"}}
# означает:
# - разрешаем CORS только для /api/*
# - разрешаем запросы с любых origin (для учебного проекта)
#
# В реальном продакшене origins ограничивают.
CORS(
    app,
    resources={r"/api/*": {"origins": "*"}}
)

# ============================================================
# 2. Вспомогательные функции
# ============================================================

def success_response(data, status_code=200):
    """
    Унифицированный успешный ответ API.
    """
    return jsonify({
        "success": True,
        "data": data,
        "error": None
    }), status_code


def error_response(message, status_code=400):
    """
    Унифицированный ответ с ошибкой.
    """
    return jsonify({
        "success": False,
        "data": None,
        "error": message
    }), status_code


def get_number_param(name):
    """
    Унифицированная функция получения числового query-параметра.

    Пример:
      /api/add?a=2&b=3

    Если параметр отсутствует или не число — бросаем ошибку.
    """
    value = request.args.get(name)

    if value is None:
        raise ValueError(f"Missing query parameter '{name}'")

    try:
        return float(value)
    except ValueError:
        raise ValueError(f"Query parameter '{name}' must be a number")


# ============================================================
# 3. Healthcheck (для Render)
# ============================================================

@app.route("/health", methods=["GET"])
def health():
    """
    Healthcheck endpoint.
    Render использует его, чтобы понимать, что сервис жив.
    """
    return jsonify({"status": "ok"}), 200


# ============================================================
# 4. API endpoints (namespace /api)
# ============================================================

@app.route("/api/add", methods=["GET"])
def add():
    """
    Сложение двух чисел.

    Пример запроса:
      GET /api/add?a=2&b=3
    """
    try:
        a = get_number_param("a")
        b = get_number_param("b")

        result = a + b

        return success_response({
            "operation": "add",
            "a": a,
            "b": b,
            "result": result
        })

    except ValueError as e:
        return error_response(str(e), 400)


@app.route("/api/multiply", methods=["GET"])
def multiply():
    """
    Умножение двух чисел.

    Пример запроса:
      GET /api/multiply?a=4&b=5
    """
    try:
        a = get_number_param("a")
        b = get_number_param("b")

        result = a * b

        return success_response({
            "operation": "multiply",
            "a": a,
            "b": b,
            "result": result
        })

    except ValueError as e:
        return error_response(str(e), 400)


@app.route("/api/divide", methods=["GET"])
def divide():
    """
    Деление двух чисел.

    Пример запроса:
      GET /api/divide?a=10&b=2
    """
    try:
        a = get_number_param("a")
        b = get_number_param("b")

        if b == 0:
            return error_response("Division by zero is not allowed", 400)

        result = a / b

        return success_response({
            "operation": "divide",
            "a": a,
            "b": b,
            "result": result
        })

    except ValueError as e:
        return error_response(str(e), 400)


# ============================================================
# 5. Обработка 404 и 500 (единый стиль ошибок)
# ============================================================

@app.errorhandler(404)
def not_found(_):
    return error_response("Endpoint not found", 404)


@app.errorhandler(500)
def internal_error(_):
    return error_response("Internal server error", 500)


# ============================================================
# 6. Точка входа (для локального запуска)
# ============================================================

# В продакшене (Render) используется Gunicorn,
# но этот блок удобен для локального запуска:
#
#   python app.py
#
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
