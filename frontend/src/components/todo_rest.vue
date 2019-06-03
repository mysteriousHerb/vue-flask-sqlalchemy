<template>
  <div id="todos-vue">
    <div>
      <label>New task:</label>
      <!-- use v-model for 2-way binding, call method when user press enter @keyup.enter-->
      <input id="new_todo" v-model="new_todo" placeholder="edit me" @keyup.enter="add_todo()">
      <button @click="update_todo(id=-1, content=new_todo, done=false, delete_=false)">Add</button>
    </div>
    <div>
      <div v-for="(todo) in todos" :key="todo.id">
        <label>{{todo.id}}.</label>
        <!-- we also want to be able to directly update the existing todo, this is handled by v-model, but our database needs to be handled differently-->
        <input v-model="todo.content" :disabled="todo.done" @change="update_todo(id=todo.id, content=todo.content, done=todo.done, delete_=false)">
        <!-- when click the checkbox, the input becomes disabled -->
        <!-- use @change rather than @click, the @click event happens too fast that new_val is not sent through  -->
        <input type="checkbox" v-model="todo.done" @change="update_todo(id=todo.id, content=todo.content, done=todo.done, delete_=false)">
        <button @click="update_todo(id=todo.id, content='', done=true, delete_=true)">Delete</button>
      </div>
      <button @click="read_todo()">refresh todo</button>
    </div>
  </div>
</template>

<script>
import { setTimeout } from "timers";
export default {
  name: "todo_comp",
  data: function() {
    return {
      new_todo: "",
      todos: [
        { id: 1, content: "", done: false},
      ],
    };
  },
  mounted: function() {
    this.read_todo();
  },
  computed: {
  },
  methods: {
    // all the methods will be replaced with REST API call later
    read_todo: function() {
      this.axios
        .get("http://localhost:5000/todo_db")
        .then(response => (this.todos = response.data));
    },
    update_todo: function(
      id = -1,
      content = "",
      done = false,
      delete_ = false
    ) {
      var data = {
         id: id, content: content, done: done, delete: delete_ 
      };
      console.log(data);
      this.axios
        .post("http://localhost:5000/todo_db", data)
        .then(() => this.read_todo());
      //   add a delay to make sure the backend respond
    },
    print:function(data){
        console.log(data)
    }
  }
};
</script>