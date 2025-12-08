from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

# In-memory storage (later will be replaced with PostgreSQL)
tasks = {}

# ------------------------------
# Task Manager Endpoints
# ------------------------------

@app.post("/tasks")
def create_task():
    data = request.json
    if not data or "title" not in data:
        return jsonify({"error": "Field 'title' is required"}), 400

    task_id = str(uuid.uuid4())
    task = {
        "id": task_id,
        "title": data["title"],
        "done": False
    }

    tasks[task_id] = task
    return jsonify(task), 201


@app.get("/tasks")
def list_tasks():
    return jsonify(list(tasks.values())), 200


@app.put("/tasks/<task_id>")
def update_task(task_id):
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404

    data = request.json or {}
    task = tasks[task_id]

    task["title"] = data.get("title", task["title"])
    task["done"] = data.get("done", task["done"])

    return jsonify(task), 200


@app.delete("/tasks/<task_id>")
def delete_task(task_id):
    if task_id not in tasks:
        return jsonify({"error": "Task not found"}), 404

    del tasks[task_id]
    return jsonify({"message": "Task deleted"}), 200


@app.get("/stats")
def stats():
    total = len(tasks)
    completed = sum(1 for t in tasks.values() if t["done"])
    return jsonify({
        "total": total,
        "completed": completed,
        "pending": total - completed
    }), 200


# ------------------------------
# Math endpoints (business logic)
# ------------------------------

@app.get("/math/add")
def add():
    a = float(request.args.get("a", 0))
    b = float(request.args.get("b", 0))
    return jsonify({"result": a + b})


@app.get("/math/multiply")
def multiply():
    a = float(request.args.get("a", 1))
    b = float(request.args.get("b", 1))
    return jsonify({"result": a * b})


@app.get("/math/divide")
def divide():
    a = float(request.args.get("a"))
    b = float(request.args.get("b"))

    if b == 0:
        return jsonify({"error": "Division by zero"}), 400

    return jsonify({"result": a / b})


# ------------------------------
# Root endpoint
# ------------------------------

@app.get("/")
def index():
    return "Task Manager API is working! 🚀"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
