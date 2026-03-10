# Flask app for Todo API
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory storage for todos
todos = [
    {"id": 1, "title": "Buy groceries", "completed": False},
    {"id": 2, "title": "Do laundry", "completed": True}
]

# Helper function to find todo by ID

def find_todo(todo_id):
    return next((todo for todo in todos if todo["id"] == todo_id), None)

# GET all todos

@app.route('/api/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

# POST a new todo

@app.route('/api/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({"error": "Title is required"}), 400
    
    new_id = max(todo["id"] for todo in todos) + 1 if todos else 1
    
    new_todo = {
        "id": new_id,
        "title": data["title"],
        "completed": data.get("completed", False)
    }
    todos.append(new_todo)
    return jsonify(new_todo), 201

# GET a specific todo

@app.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = find_todo(todo_id)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify(todo)



















# PUT (update) a todo

@app.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = find_todo(todo_id)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if 'title' in data:
        todo['title'] = data['title']
    if 'completed' in data:
        todo['completed'] = data['completed']
    
    return jsonify(todo)

# DELETE a todo

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    global todos
    todo = find_todo(todo_id)
    if todo is None:
        return jsonify({"error": "Todo not found"}), 404
    
    todos = [t for t in todos if t["id"] != todo_id]
    return jsonify({"message": "Todo deleted"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)
