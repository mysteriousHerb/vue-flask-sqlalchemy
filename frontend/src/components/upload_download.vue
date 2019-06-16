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
            :useCustomSlot="true"
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
          <v-btn @click="toggle">toggle</v-btn>
        </v-flex>
      </v-layout>
      <br>
      <v-layout align-center justify-center>
        <v-flex xs10>
          <!-- use :key to actively refresh this component https://michaelnthiessen.com/force-re-render -->
          <v-img :src="image_location" :key="active_file"/>
        </v-flex>
      </v-layout>

      <v-layout align-center justify-center>
        <v-flex xs4>
          <v-list>
            <v-list-tile
              v-for="file in existing_files"
              :key="file"
              @click="change_file(file)"
            >
              <v-list-tile-content>
                <v-list-tile-title v-text="file"></v-list-tile-title>
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
import FileSaver from "file-saver";

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
      existing_files: [],
      active_file: "default.jpg"
    };
  },
  computed: {
    image_location: function() {
      return this.$API_URL + "/download_file/" + this.active_file;
    }
  },
  mounted: function() {
    this.read_existing_files();
  },
  methods: {
    toggle: function() {
      console.log(this.existing_files)
      this.axios({
        url: this.$API_URL + "/verify_descriptor",
        method: "POST",
        data: { user: "test", descriptor: [1, 2, 3, 4, 5, 6] }
      }).then(response => {
        var descriptor_json = {
          descriptor_user: response.data["descriptor_user"],
          salt2: response.data["salt2"]
        };
        console.log(descriptor_json);
        // https://stackoverflow.com/questions/16329293/save-json-string-to-client-pc-using-html5-api
        // JSON.parse() takes a JSON string and transforms it into a JavaScript object.
        // JSON.stringify() takes a JavaScript object and transforms it into a JSON string.
        // NOTE: Javascript object needs to be JSON (a string) to communicate
        var descriptor_json = JSON.stringify(descriptor_json);
        var blob = new Blob([descriptor_json], { type: "application/json" });
        FileSaver.saveAs(blob, "key.json");
      });
    },
    read_existing_files: function() {
       this.axios({
        url: this.$API_URL + "/existing_files",
        method: "GET"
      }).then(response => {this.existing_files = response.data}) 
    },

    removeAllFiles: function() {
      this.$refs.myVueDropzone.removeAllFiles();
      console.log(this.$API_URL);
    },
    upload_complete: function(file) {
      console.log("uploaded");
      console.log(file["name"]);
    },
    remove_file: function(file) {
      // https://alligator.io/vuejs/rest-api-axios/
      this.axios({
        url: this.$API_URL + "/upload_file",
        method: "POST",
        data: {
          remove_file: file["name"]
        }
      }).then(response => {});
    },
    download_file: function() {
      // https://thewebtier.com/snippets/download-files-with-axios/
      this.axios({
        url: this.image_location,
        method: "GET",
        responseType: "blob" // important
      }).then(response => {
        // CORS headings - see backend
        var filename = response.headers["x-suggested-filename"];
        var filetype = response.headers["x-suggested-filetype"];

        // var blob = new Blob([response.data], { type: "image/png" });
        FileSaver.saveAs(new Blob([response.data]), filename + "." + filetype);
      });
    },
    change_file: function(name) {
      this.active_file = name;
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
