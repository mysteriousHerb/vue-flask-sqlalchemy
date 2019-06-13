<template>
  <div class="todo">
      <FaceDetection/>
  </div>
</template>

<script>
// @ is an alias to /src
import FaceDetection from '@/components/FaceDetection.vue'


export default {
  name: 'face',
  components: {
    FaceDetection
  }
}
</script>
