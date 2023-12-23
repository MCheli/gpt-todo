<template>
  <div class="container">
    <h1 class="header">//TODO:</h1>
    <div class="input-group mb-3">
      <input v-model="newTodo" type="text" class="form-control" placeholder="Enter a new todo">
      <button @click="addTodo" class="btn btn-primary">Add</button>
    </div>
    <ul class="list-group">
      <li v-for="(todo, index) in todos" :key="todo.id" class="list-group-item" draggable="true"
        @dragstart="dragStart(index)" @drop="drop" @dragover.prevent="draggedOverIndex = index">
        <div class="checkmark" @click="deleteTodo(todo.id)"></div>
        <span :class="['todo-title', { 'checked': todo.completed }]">{{ todo.title }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      todos: [],
      newTodo: '',
      draggingIndex: null,
      draggedOverIndex: null
    };
  },
  mounted() {
    this.getTodos();
  },
  methods: {
    async getTodos() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/todos');
        this.todos = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async addTodo() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/api/todos', { title: this.newTodo });
        this.todos.push(response.data);
        this.newTodo = '';
      } catch (error) {
        console.error(error);
      }
    },
    async deleteTodo(todoId) {
      try {
        await axios.delete(`http://127.0.0.1:5000/api/todos/${todoId}`);
        this.todos = this.todos.filter(todo => todo.id !== todoId);
      } catch (error) {
        console.error(error);
      }
    },
    dragStart(index) {
      this.draggingIndex = index;
    },
    drop() {
      if (this.draggingIndex === this.draggedOverIndex) return;

      const draggedTodo = this.todos[this.draggingIndex];
      this.todos.splice(this.draggingIndex, 1);
      this.todos.splice(this.draggedOverIndex, 0, draggedTodo);

      this.updateTodoOrder();
    },
    async updateTodoOrder() {
      try {
        await axios.post('http://127.0.0.1:5000/api/todos/reorder', this.todos);
        // Optional: Show a success message or perform any additional actions
      } catch (error) {
        console.error(error);
      }
    }
  }
};
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Bungee+Shade&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Open+Sans&display=swap');

.container {
  margin-top: 30px;
  background-color: #fff;
  padding: 20px;
  border-radius: 5px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.1);
}

.header {
  font-family: 'Bungee Shade', cursive;
  color: #333;
  text-align: center;
  margin-bottom: 20px;
}

.input-group {
  display: flex;
  justify-content: center;
}

.form-control {
  width: 70%;
  border-radius: 5px 0 0 5px;
  border: none;
  padding: 10px;
  font-size: 16px;
  font-family: 'Open Sans', sans-serif;
}

.btn-primary {
  border-radius: 0 5px 5px 0;
  border: none;
  padding: 10px 20px;
  font-size: 16px;
  background-color: #007bff;
  color: #fff;
  font-family: 'Open Sans', sans-serif;
}

.list-group-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border: none;
  background-color: #f8f9fa;
  margin-top: 5px;
  border-radius: 5px;
  box-shadow: 0px 2px 4px rgba(0, 0, 0, 0.2);
}

.checkmark {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid #333;
  margin-right: 10px;
  cursor: pointer;
}

.todo-title {
  flex-grow: 1;
  color: #333;
  text-decoration: none;
  font-family: 'Open Sans', sans-serif;
}

.list-group-item:hover {
  background-color: #e9ecef;
}

.list-group-item .checked {
  text-decoration: line-through;
  color: #888;
}

</style>