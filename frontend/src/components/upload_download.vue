<template>
  <div>
    <vueDropzone
      ref="myVueDropzone"
      id="myVueDropzone"
      @vdropzone-success="upload_complete"
      @vdropzone-removed-file="cancel_upload"
      :options="dropzoneOptions"
      :useCustomSlot="false"
    >
      <div class="dropzone-custom-content">
        <h3 class="dropzone-custom-title">Drag and drop to upload content!</h3>
        <div class="subtitle">...or click to select a file from your computer</div>
      </div>
    </vueDropzone>

    <!-- custom function called with buttons -->
    <button @click="removeAllFiles">Remove All Files</button>
    <button @click="download_file"> Download file</button>
    <br/>
    <img src="http://localhost:5000/download_file"/>
  </div>
</template>

<script>
import vue2Dropzone from "vue2-dropzone";
import "vue2-dropzone/dist/vue2Dropzone.min.css";
// import axios from "axios";

export default {
  name: "upload_download",
  components: {
      // https://itnext.io/vue-a-pattern-for-idiomatic-performant-component-registration-you-might-not-know-about-9f3c091846f5?gi=4351204c93b8
  //  https://stackoverflow.com/questions/52038615/in-vue-js-why-do-we-have-to-export-components-after-importing-them
    // https://alligator.io/vuejs/vue-dropzone/
    // https://rowanwins.github.io/vue-dropzone/docs/dist/#/events
    vueDropzone: vue2Dropzone,
  },
  methods: {
    removeAllFiles() {
      this.$refs.myVueDropzone.removeAllFiles();
    },
    upload_complete(file, response) {
      console.log("uploaded");
      console.log(file['name']);
    },
    cancel_upload(file, error, xhr) {
      console.log("cancelled upload");
      console.log(file['name']);
      // https://alligator.io/vuejs/rest-api-axios/
      this.axios({
        url: "http://localhost:5000/upload_file",
        method: "POST",
        data: {
          file: '',
          cancel_file: file["name"],
        },
      }).then(response => {console.log(response)});
    },
    download_file(filename='download') {
      // https://www.tutorialspoint.com/How-to-import-a-Python-module-given-the-full-path
      this.axios({
        url: "http://localhost:5000/download_file",
        method: "GET",
        responseType: "blob" // important
      }).then(response => {
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        console.log(response)
        link.href = url;
        // Filename seems to have to be changed unless otherwise provided
        // the extension can be automatically decided
        link.setAttribute("download", filename + '.' + response.data.type.split("/")[1]); 
        document.body.appendChild(link);
        link.click();
      });
    }
  },

  data: function() {
    return {
      // dropzone settings
      dropzoneOptions: {
        url: "http://localhost:5000/upload_file",
        addRemoveLinks: true,
        thumbnailWidth: 150,
        maxFilesize: 0.5,
        maxFiles: 4,
        dictDefaultMessage: "<i class='fa fa-cloud-upload'></i>UPLOAD ME"
      }
    };
  }
};
</script>

<style scope>
@import url("https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css");

.dropzone-custom-title {
  margin-top: 0;
  color: #00b782;
}

.subtitle {
  color: #314b5f;
}
</style>
