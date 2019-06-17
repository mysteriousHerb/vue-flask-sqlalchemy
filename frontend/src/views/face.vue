<template>
  <div class="todo">
    <FaceDetection/>
    <UploadDescriptor/>
  </div>
</template>

<script>
// @ is an alias to /src
import FaceDetection from "@/components/FaceDetection.vue";
import UploadDescriptor from "@/components/UploadDescriptor.vue";

export default {
  name: "face",
  components: {
    FaceDetection,
    UploadDescriptor
  },
  mounted: function(){
    this.initialize_folders();
  },
  methods: {
    initialize_folders: function() {
      this.axios({
        url: this.$API_URL + "/initialize_folders",
        method: "POST",
        data: { initialize_folders: true }
      });
    }
  }
};
</script>
