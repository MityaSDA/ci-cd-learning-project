from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Твоя оригинальная функция
def add(a, b):
    return a + b

# HTTP-маршрут, чтобы Render мог работать
@app.route("/")
def home():
    return "CI/CD pipeline is working!"

@app.route("/add")
def add_route():
    try:
        a = float(request.args.get("a", 0))
        b = float(request.args.get("b", 0))
        return jsonify({"result": add(a, b)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render требует 10000
    app.run(host="0.0.0.0", port=port)
