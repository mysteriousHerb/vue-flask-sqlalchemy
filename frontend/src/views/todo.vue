<template>
  <div class="todo">
      <todo_rest/>
  </div>
</template>

<script>
// @ is an alias to /src
import todo_comp from '@/components/todo_comp.vue'
import todo_rest from '@/components/todo_rest.vue'


export default {
  name: 'todo',
  components: {
    todo_comp,
    todo_rest
  }
}
</script>
