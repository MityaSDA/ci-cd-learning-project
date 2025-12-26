"""
backend/app.py

Основной файл backend-приложения.

Назначение:
- Flask API
- CORS для frontend (React)
- API namespace /api/*
- Middleware-подход:
  - валидация входных данных
  - единый формат ответов
  - единый формат ошибок

Проект учебный, но структура максимально приближена к production.
"""

# ============================================================
# 0. Импорты
# ============================================================

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
# потому что frontend и backend работают
# на РАЗНЫХ доменах:
#
# frontend (dev):
#   http://localhost:3000
#
# backend (Render):
#   https://*.onrender.com
#
# Если CORS не включить — браузер БЛОКИРУЕТ запросы
#
# resources={r"/api/*": {"origins": "*"}}
# означает:
# - CORS разрешён ТОЛЬКО для /api/*
# - origins="*" — разрешаем все источники (для обучения)
#
# ⚠️ В реальном продакшене origins ограничивают
#
CORS(
    app,
    resources={r"/api/*": {"origins": "*"}}
)

# ============================================================
# 2. Унифицированные ответы API
# ============================================================

def success_response(data, status_code=200):
    """
    Унифицированный успешный ответ API.

    Все успешные ответы backend выглядят одинаково:

    {
        "success": true,
        "data": {...},
        "error": null
    }
    """
    return jsonify({
        "success": True,
        "data": data,
        "error": None
    }), status_code


def error_response(message, status_code=400):
    """
    Унифицированный ответ с ошибкой.

    Все ошибки backend выглядят одинаково:

    {
        "success": false,
        "data": null,
        "error": "Сообщение об ошибке"
    }
    """
    return jsonify({
        "success": False,
        "data": None,
        "error": message
    }), status_code


# ============================================================
# 3. Middleware / Вспомогательная логика
# ============================================================

def get_number_param(name):
    """
    Унифицированная функция получения числового query-параметра.

    Используется ВСЕМИ API-эндпоинтами.

    Пример запроса:
      /api/add?a=2&b=3

    Что делает:
    1. Проверяет, что параметр существует
    2. Преобразует в float
    3. В случае ошибки — бросает ValueError
    """
    value = request.args.get(name)

    if value is None:
        raise ValueError(f"Missing query parameter '{name}'")

    try:
        return float(value)
    except ValueError:
        raise ValueError(f"Query parameter '{name}' must be a number")


# ============================================================
# 4. Healthcheck (Render использует его)
# ============================================================

@app.route("/health", methods=["GET"])
def health():
    """
    Healthcheck endpoint.

    Render периодически обращается к этому URL,
    чтобы понять, что сервис жив.

    Если endpoint возвращает 200 — сервис считается healthy.
    """
    return jsonify({"status": "ok"}), 200


# ============================================================
# 5. API endpoints (/api/*)
# ============================================================

@app.route("/api/add", methods=["GET"])
def add():
    """
    Сложение двух чисел.

    Пример:
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

    Пример:
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

    Пример:
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
# 6. Глобальные обработчики ошибок
# ============================================================

@app.errorhandler(404)
def not_found(_):
    """
    Любой неизвестный endpoint.
    """
    return error_response("Endpoint not found", 404)


@app.errorhandler(500)
def internal_error(_):
    """
    Любая необработанная ошибка сервера.
    """
    return error_response("Internal server error", 500)


# ============================================================
# 7. Локальный запуск (не используется в Render)
# ============================================================

# В Render backend запускается через Gunicorn,
# но этот блок полезен для локальной отладки:
#
#   python app.py
#
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)
