from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient
import uuid
from bson import ObjectId

app = Flask(__name__)
CORS(app)

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['todo_app']
todos_collection = db['todos']

@app.route('/api/todos', methods=['GET'])
def get_todos():
    todos = list(todos_collection.find())
    # Convert ObjectId to string
    todos = [{**todo, '_id': str(todo['_id'])} for todo in todos]
    return jsonify(todos)

@app.route('/api/todos', methods=['POST'])
def add_todo():
    todo = request.json
    todo['id'] = str(uuid.uuid4())  # Generate a unique ID for the todo item
    todos_collection.insert_one(todo)
    # Convert ObjectId to string
    todo['_id'] = str(todo['_id'])
    return jsonify(todo), 201

@app.route('/api/todos/<string:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todos_collection.delete_one({'id': todo_id})
    return jsonify({'message': 'Todo deleted'})

@app.route('/api/todos/reorder', methods=['POST'])
def reorder_todos():
    reordered_todos = request.json
    todos_collection.drop()
    todos_collection.insert_many(reordered_todos)
    return jsonify({'message': 'Todos reordered'})

if __name__ == '__main__':
    app.run(debug=True)