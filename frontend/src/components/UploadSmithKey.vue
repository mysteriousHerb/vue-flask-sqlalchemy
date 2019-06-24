<template>
  <div>
    <v-container fluid>
      <v-layout align-center justify-center row fill-height>
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
    </v-container>
  </div>
</template>

<script>
import vue2Dropzone from "vue2-dropzone";
import "vue2-dropzone/dist/vue2Dropzone.min.css";

// import axios from "axios";

export default {
  name: "UploadSmithKey",
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
        url: this.$API_URL + "/upload_smith_key",
        addRemoveLinks: true,
        thumbnailWidth: 150,
        maxFilesize: 0.5,
        maxFiles: 1
      }
    };
  },
  computed: {
    session_id() {
      // session_id should be sent to all the axios request to backend now
      return this.$store.state.session_id;
    },
    user_name_in_key(){
      return this.$store.state.user_name_in_key;
    }
  },
  mounted: function() {
  },
  methods: {
    upload_smith_key: function(file, xhr, formData) {
      formData.append("session_id", this.session_id);
    },
    remove_file: function(file) {
      // https://alligator.io/vuejs/rest-api-axios/
      // https://github.com/rowanwins/vue-dropzone/issues/85
      if (this.$refs.myVueDropzone.dropzone.disabled !== true) {
        console.log("remove file");
        this.axios({
          url: this.$API_URL + "/upload_descriptor",
          method: "POST",
          data: {
            remove_file: file["name"]
          }
        }).then(response => {});
      }
    },
    success_upload_key:function(file, response){
      console.log(response)
      if (response['message'] == "key uploaded successfully"){
        // send the user_name to vuex store
        this.$store.dispatch('update_user_name_in_key', response['user_name'])
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
