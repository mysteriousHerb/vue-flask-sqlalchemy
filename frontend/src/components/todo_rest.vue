<template>
  <div>
    <v-container grid-list-md text-xs-center>
      <v-layout align-center justify-center>
        <v-flex>
          <v-btn large dark color="green" @click="read_todo()">
            <v-icon dark>
              refresh
              <v-icon>{{route.icon}}</v-icon>
            </v-icon>Fetch database
          </v-btn>
        </v-flex>
        <v-progress-circular :value="progress"></v-progress-circular>
        <span>Progress so far</span>
        <v-flex></v-flex>
      </v-layout>

      <v-layout align-center justify-center>
        <v-flex xs8>
          <!-- use v-model for 2-way binding, call method when user press enter @keyup.enter-->
          <!-- <v-text-field v-model="new_todo" placeholder="edit me" @keyup.enter="add_todo()"> -->
          <v-text-field
            v-model="new_todo"
            placeholder="edit me"
            label="New Task"
            clearable
            @keydown.enter="update_todo(id=-1, content=new_todo, done=false, delete_=false)"
          ></v-text-field>
        </v-flex>
        <v-flex xs1/>
        <v-flex xs1>
          <v-btn
            small
            fab
            dark
            color="teal"
            @click="update_todo(id=-1, content=new_todo, done=false, delete_=false)"
          >
            <v-icon dark>add</v-icon>
          </v-btn>
        </v-flex>
      </v-layout>

      <div v-for="(todo) in todos" :key="todo.id">
        <v-layout align-center justify-center>
          <v-flex xs8>
            <!-- we also want to be able to directly update the existing todo, this is handled by v-model, but our database needs to be handled differently-->
            <v-text-field
              v-model="todo.content"
              :label="String(todo.id)"
              :disabled="todo.done"
              @change="update_todo(id=todo.id, content=todo.content, done=todo.done, delete_=false)"
            />
          </v-flex>
          <v-flex xs1>
            <!-- when click the checkbox, the input becomes disabled -->
            <!-- use @change rather than @click, the @click event happens too fast that new_val is not sent through  -->
            <v-switch
              v-model="todo.done"
              label="Done?"
              @change="update_todo(id=todo.id, content=todo.content, done=todo.done, delete_=false)"
            />
          </v-flex>
          <v-flex xs1>
            <v-btn
              small
              fab
              dark
              color="error"
              @click="update_todo(id=todo.id, content='', done=true, delete_=true)"
            >
              <v-icon dark>remove</v-icon>
            </v-btn>
          </v-flex>
        </v-layout>
      </div>
    </v-container>
  </div>
</template>

<script>
export default {
  name: "todo_comp",
  data: function() {
    return {
      new_todo: "",
      todos: [{ id: 1, content: "", done: false }]
    };
  },
  mounted: function() {
    this.read_todo();
  },
  computed: {
    progress: function() {
      var task_done = this.todos.filter(todo => todo.done);
      // console.log(task_done)
      return (task_done.length / this.todos.length) * 100;
    }
  },
  methods: {
    // all the methods will be replaced with REST API call later
    read_todo: function() {
      this.axios
        .get(this.$API_URL + "/todo_db")
        .then(response => (this.todos = response.data));
    },
    update_todo: function(
      id = -1,
      content = "",
      done = false,
      delete_ = false
    ) {
      var data = {
        id: id,
        content: content,
        done: done,
        delete: delete_
      };
      // console.log(data);
      this.axios
        .post(this.$API_URL + "/todo_db", data)
        .then(() => this.read_todo());
      //   add a delay to make sure the backend respond
    },
  }
};
</script>