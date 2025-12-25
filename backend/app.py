from flask import Flask, jsonify, request
from flask_cors import CORS

# Создаём Flask-приложение
app = Flask(__name__)

# ВКЛЮЧАЕМ CORS (критично для React)
CORS(app)

# --------------------
# Health check
# --------------------
@app.route("/health", methods=["GET"])
def health():
    return jsonify(status="ok")


# --------------------
# Add: /add?a=2&b=3
# --------------------
@app.route("/add", methods=["GET"])
def add():
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)

    if a is None or b is None:
        return jsonify(error="Parameters a and b are required"), 400

    return jsonify(result=a + b)


# --------------------
# Multiply: /multiply?a=4&b=5
# --------------------
@app.route("/multiply", methods=["GET"])
def multiply():
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)

    if a is None or b is None:
        return jsonify(error="Parameters a and b are required"), 400

    return jsonify(result=a * b)


# --------------------
# Divide: /divide?a=10&b=2
# --------------------
@app.route("/divide", methods=["GET"])
def divide():
    a = request.args.get("a", type=float)
    b = request.args.get("b", type=float)

    if a is None or b is None:
        return jsonify(error="Parameters a and b are required"), 400

    if b == 0:
        return jsonify(error="Division by zero"), 400

    return jsonify(result=a / b)


# --------------------
# Entry point
# --------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
