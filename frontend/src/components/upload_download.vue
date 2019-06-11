<template>
  <div>
    <v-container grid-list-md text-xs-center fluid>
      <v-layout align-center justify-center>
        <v-flex xs12>
          <vueDropzone
            ref="myVueDropzone"
            id="myVueDropzone"
            @vdropzone-success="upload_complete"
            @vdropzone-removed-file="remove_file"
            :options="dropzoneOptions"
            :useCustomSlot="false"
          >
            <div class="dropzone-custom-content">
              <h3 class="dropzone-custom-title">Drag and drop to upload content!</h3>
              <div class="subtitle">...or click to select a file from your computer</div>
            </div>
          </vueDropzone>
        </v-flex>
      </v-layout>
      <v-layout>
        <v-flex>
          <!-- custom function called with buttons -->
          <v-btn @click="removeAllFiles">Remove All Files</v-btn>

          <v-btn @click="download_file">Download file</v-btn>
        </v-flex>
      </v-layout>
      <br>
      <v-layout align-center justify-center>
        <v-flex xs10>
          <v-img :src="image_location"/>
        </v-flex>
      </v-layout>

      <v-layout align-center justify-center>
        <v-flex xs4>
          <v-list>
            <v-list-tile v-for="file in existing_files" :key="file.index" @click="change_file(file.name)">
              <v-list-tile-content>
                <v-list-tile-title v-text="file.name"></v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </v-list>
        </v-flex>
      </v-layout>
    </v-container>
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
    vueDropzone: vue2Dropzone
  },
  data: function() {
    return {
      // dropzone settings
      dropzoneOptions: {
        url: this.$API_URL + "/upload_file",
        addRemoveLinks: true,
        thumbnailWidth: 150,
        maxFilesize: 0.5,
        maxFiles: 4,
        dictDefaultMessage: "<i class='fa fa-cloud-upload'></i>UPLOAD ME"
      },
      existing_files: [{ name: "", filepath: "", active: false},],
      image_location: this.$API_URL + "/download_file",
    };
  },
  mounted: function() {
    this.read_existing_files();
  },
  methods: {
    read_existing_files: function() {
      this.axios({
        url: this.$API_URL + "/download_file",
        method: "POST",
        data: { index_files: true }
      }).then(response => (this.existing_files = response.data));
    },

    // removeAllFiles: function() {
    //   this.$refs.myVueDropzone.removeAllFiles();
    // },
    upload_complete: function(file, response) {
      console.log("uploaded");
      console.log(file["name"]);
    },
    remove_file: function(file, error, xhr) {
      // https://alligator.io/vuejs/rest-api-axios/
      this.axios({
        url: this.$API_URL + "/upload_file",
        method: "POST",
        data: {
          remove_file: file["name"]
        }
      }).then(response => {});
    },
    download_file: function(filename = "download") {
      // https://thewebtier.com/snippets/download-files-with-axios/
      this.axios({
        url: this.$API_URL + "/download_file",
        method: "GET",
        responseType: "blob" // important
      }).then(response => {
        // CORS headings - see backend
        var filename = response.headers["x-suggested-filename"];
        var filetype = response.headers["x-suggested-filetype"];
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement("a");
        console.log(response);
        link.href = url;
        // Filename seems to have to be changed unless otherwise provided
        // the extension can be automatically decided
        link.setAttribute("download", filename + filetype);
        document.body.appendChild(link);
        link.click();
      });
    },
    change_file: function(name='test.jpg') {
      this.axios({
        url: this.$API_URL + "/download_file",
        method: "POST",
        data: { change_file: name}
      })
    }
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
