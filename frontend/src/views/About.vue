<template>
  <div class="about">
    <h1>This is an about page</h1>
  <upload_download/>
  </div>
</template>



<script>
// @ is an alias to /src
import upload_download from '@/components/upload_download.vue'


export default {
  name: 'About',
  components: {
    upload_download
  }
}
</script>
