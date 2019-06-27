<template>
  <div>
    <v-container fluid>
      <v-layout :style="{'margin-top': '100px'}" align-center justify-center>
        <v-flex xs8>
          <label class="display-3">Upload your .smith key </label>
          <v-fa-icon name="key" scale="3"/>
          <v-fa-icon name="arrow-circle-down" scale="3"/>
        </v-flex>
      </v-layout>

      <v-layout>
        <v-dialog v-model="error_key" width="500">
          <v-card>
            <v-card-text class="display-1" style="color:black">
              Your Smith key is corrupted, try again.
              <v-fa-icon name="times-circle" scale="2"/>
            </v-card-text>
            <v-divider></v-divider>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="primary" flat @click="error_key = false">OK</v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-layout>

      <v-layout align-center justify-center>
        <v-flex xs8>
          <vueDropzone
            ref="myVueDropzone"
            id="myVueDropzone"
            @vdropzone-sending="upload_smith_key"
            @vdropzone-removed-file="remove_file"
            @vdropzone-success="success_upload_key"
            :options="dropzoneOptions"
            :useCustomSlot="true"
          >
            <div class="dropzone-custom-content">
              <h3 class="dropzone-custom-title">Drag and drop your smith key!</h3>
              <div class="subtitle">...or click to select a file from your computer</div>
            </div>
          </vueDropzone>
        </v-flex>
      </v-layout>
      <v-layout></v-layout>
    </v-container>
  </div>
</template>

<script>
import vue2Dropzone from "vue2-dropzone";
import "vue2-dropzone/dist/vue2Dropzone.min.css";
import Icon from "vue-awesome/components/Icon";

// import axios from "axios";

export default {
  name: "UploadSmithKey",
  components: {
    // https://itnext.io/vue-a-pattern-for-idiomatic-performant-component-registration-you-might-not-know-about-9f3c091846f5?gi=4351204c93b8
    //  https://stackoverflow.com/questions/52038615/in-vue-js-why-do-we-have-to-export-components-after-importing-them
    // https://alligator.io/vuejs/vue-dropzone/
    // https://rowanwins.github.io/vue-dropzone/docs/dist/#/events
    vueDropzone: vue2Dropzone,
    "v-fa-icon": Icon
  },
  data: function() {
    return {
      // dropzone settings
      dropzoneOptions: {
        url: this.$API_URL + "/upload_smith_key",
        addRemoveLinks: true,
        thumbnailWidth: 150,
        maxFilesize: 0.5,
        maxFiles: 1
      },
      error_key: false,
    };
  },
  computed: {
    session_id() {
      // session_id should be sent to all the axios request to backend now
      return this.$store.state.session_id;
    },
    user_name_in_key() {
      return this.$store.state.user_name_in_key;
    }
  },
  mounted: function() {},
  methods: {
    upload_smith_key: function(file, xhr, formData) {
      formData.append("session_id", this.session_id);
    },
    remove_file: function(file) {
      // https://alligator.io/vuejs/rest-api-axios/
      // https://github.com/rowanwins/vue-dropzone/issues/85
      // if (this.$refs.myVueDropzone.dropzone.disabled !== true) {
      //   console.log("remove file");
      //   this.axios({
      //     url: this.$API_URL + "/upload_descriptor",
      //     method: "POST",
      //     data: {
      //       remove_file: file["name"]
      //     }
      //   }).then(response => {});
      // }
      console.log('remove keys')
    },
    success_upload_key: function(file, response) {
      console.log(response);
      if (response["message"] == "key uploaded successfully") {
        // send the user_name to vuex store
        this.$store.dispatch("update_user_name_in_key", response["user_name"]);
      } else {
        this.error_key = true;
        this.$refs.myVueDropzone.removeAllFiles()
      }
    }
  }
};
</script>

<style scope>
@import url("https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css");

.dropzone-custom-title {
  /* margin-top: 0; */
  color: #00b782;
}

.subtitle {
  color: #314b5f;
}
</style>
