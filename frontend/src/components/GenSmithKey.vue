<template>
  <div>
    <v-container fluid>
      <v-layout justify-center>
        <video
          id="video"
          ref="video"
          :width="display_size.width"
          :height="display_size.height"
          autoplay
          @play="detect_and_draw_faces"
        ></video>

        <canvas id="canvas" ref="canvas" :width="display_size.width" :height="display_size.height"/>
        <canvas
          id="canvas_capture"
          ref="canvas_capture"
          :width="display_size.width"
          :height="display_size.height"
        />
      </v-layout>
      <!-- an empty layout to create correct margin for following elements -->
      <v-layout :style="{'margin-top': margin_top}"/>
      <v-layout justify-center>
      <v-flex xs2>

            <v-text-field
            label="Your name here:"
            v-model="user_name"
          ></v-text-field>
          </v-flex>

        <v-flex xs1>
          <v-btn round color="primary"  @click="take_photo_and_upload" :disabled="!detected  || user_name===''">
            <v-icon>camera_alt</v-icon>Take photo
          </v-btn>
        </v-flex>
      </v-layout>

      <v-layout justify-center>
        <v-flex xs8>
          <!-- disabled fro now -->
          <vueDropzone
            v-if="false"
            ref="myVueDropzone"
            id="myVueDropzone"
            @vdropzone-sending="upload_photo"
            @vdropzone-removed-file="remove_file"
            :options="dropzoneOptions"
            :useCustomSlot="true"
          >
            <div class="dropzone-custom-content">
              <h3 class="dropzone-custom-title">Upload a photo!</h3>
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
import FileSaver from "file-saver";
import { stringify } from "querystring";
import * as faceapi from "face-api.js";

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
        url: this.$API_URL + "/generate_smith_key",
        addRemoveLinks: true,
        thumbnailWidth: 150,
        maxFilesize: 0.5,
        maxFiles: 1
      },
      display_size: { width: 640, height: 480 },
      margin_top: "0px",
      detections: undefined,
      user_name: '',
    };
  },
  computed: {
    detected: function(){
      if (this.detections){
        return true
      }
      else{
        return false
      }
    },
    session_id() {
      // session_id should be sent to all the axios request to backend now
      return this.$store.state.session_id;
    }
  },
  mounted: function() {
    this.load_faceapi_models();
    this.start_video();
    this.find_margin();
  },
  methods: {
    find_margin: function() {
      // var box = this.$refs.video.getBoundingClientRect();
      // this.margin_top = String(box.bottom-box.top) + "px";
      this.margin_top = String(this.display_size.height + 20) + "px";
    },
    start_video: function() {
      navigator.getUserMedia(
        { video: {} },
        stream => (video.srcObject = stream),
        err => console.error(err)
      );
    },
    load_faceapi_models: function() {
      // save the models to the public/models
      // faceapi.nets.ssdMobilenetv1.loadFromUri("/models"),
      Promise.all([
        faceapi.nets.tinyFaceDetector.loadFromUri("/models"),
        faceapi.nets.faceLandmark68Net.loadFromUri("/models"),
        faceapi.nets.faceExpressionNet.loadFromUri("/models")
      ]).then(console.log("model loaded"));
    },
    detect_and_draw_faces: function() {
      console.log("start detecting faces");
      // https://michaelnthiessen.com/this-is-undefined/
      // https://stackoverflow.com/questions/47148363/when-to-use-vm-or-this-in-vue-js
      // arrow function is a pain in vue.js and this async function also seems to cause problem
      let self = this;

      setInterval(async function() {
        //  After face detection and facial landmark prediction the face descriptors
        //  all the results are stored in self.detections
        self.detections = await faceapi
          .detectSingleFace(
            self.$refs.video,
            new faceapi.TinyFaceDetectorOptions()
          )
          .withFaceLandmarks();

        if (self.detected) {
          // calculated the size that is on our canvas size
          const resizedDetections = faceapi.resizeResults(
            self.detections,
            self.display_size
          );

          // replace the result with scaled one, all the other information will remain
          self.detections = resizedDetections;
          self.draw_face_box();
        }

        //  clear the canvas if not detected
       else{
        self.$refs.canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
        }

      }, self.refresh_time);
    },
    draw_face_box: function() {
      const canvas = this.$refs.canvas;
      canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);

      // Draw box around the face with 1 line text
      const box = this.detections.detection.box;
      // mirror X
      const box_X_flipped = {
        x: canvas.width - box.x - box.width,
        y: box.y,
        width: box.width,
        height: box.height
      };
      // see DrawBoxOptions below
      var label = 'Hello, Please type your name first'
      if (this.user_name !== ''){
        label = "Hello " + this.user_name + "! Press save to generate your key!"
      }
      const boxOptions = {
        label: label,
        lineWidth: 4,
        boxColor: "rgba(57,255,20,0.8)"
      };
      // flip the x-value x, y, width, height
      const drawBox = new faceapi.draw.DrawBox(box_X_flipped, boxOptions);
      drawBox.draw(canvas);
    },
    take_photo_and_upload: function() {
      // https://x-team.com/blog/webcam-capture-vue/
      let self = this;
      if (self.detected) {
        // keep track how many images we have captured
        const canvas = self.$refs.canvas_capture;
        var context = canvas.getContext("2d");
        context.clearRect(0, 0, canvas.width, canvas.height);
        var box = self.detections.detection.box;
        // giving some padding so we dont crop too much which gives problem to backend
        var pad = 0.2 * box.width;
        // drawImage from the video stream, with cropping
        // Sending the face with cropped region 
        // drawImage from the video stream, with cropping
        context.drawImage(
          self.$refs.video,
          box.x,
          box.y,
          box.width,
          box.height,
          box.x,
          box.y,
          box.width,
          box.height
        );

        // sending the face_location to backend to save some repetition 
        // top, right, bottom, left
        const face_location = [box.top, box.right, box.bottom, box.left]


        // Saving canvas to local drive is easy: https://github.com/eligrey/FileSaver.js/
        self.$refs.canvas_capture.toBlob(async function(blob) {
          // upload Blob as a form to the flask backend and generate descriptors
          // https://github.com/pagekit/vue-resource/blob/master/docs/recipes.md
          let formData = new FormData();
          // formData.append(name, value, filename);
          formData.append(
            "file",
            blob,
            "known_face.jpg"
          );
          formData.append(
            "user_name",
            self.user_name
          )
          formData.append("session_id", self.session_id);
          formData.append("face_location", face_location);

          self.axios({
            url: self.$API_URL + "/generate_smith_key",
            method: "POST",
            data: formData
          }).then(response=>{
            console.log('downloading .smith key')
            const json_file = JSON.stringify(response.data);
            var blob = new Blob([json_file], { type: "application/json" });
            FileSaver.saveAs(blob, self.user_name + ".smith");
            // refresh the page
            location.reload();
          });
        });
      }
    },
    upload_photo: function(file, xhr, formData) {
      formData.append("session_id", this.session_id);
        formData.append(
            "user_name",
            this.user_name
          )
    },
    remove_file: function(file) {
      // https://alligator.io/vuejs/rest-api-axios/
      // https://github.com/rowanwins/vue-dropzone/issues/85
      if (this.$refs.myVueDropzone.dropzone.disabled !== true) {
        console.log("remove file");
        this.axios({
          url: this.$API_URL + "/generate_smith_key",
          method: "POST",
          data: {
            remove_file: file["name"]
          }
        }).then(response => {});
      }
    }
  }
};
</script>

<style scoped>
@import url("https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css");

#video {
  /* position: absolute; */
  /* flip the image so it is more natural */
  position: absolute;
  transform: scaleX(-1);
  z-index: 1;
}

#canvas {
  position: absolute;
  pointer-events: none;
  z-index: 2;
  /* transform: scaleX(-1); */
}

#canvas_capture {
  /* we dont need to see it */
  position: absolute;
  display: none;
  z-index: 3;
  transform: scaleX(-1);
}

#myVueDropzone {
  position: relative;
  z-index: 0;
}

.dropzone-custom-title {
  /* margin-top: 0; */
  color: #00b782;
}

.subtitle {
  color: #314b5f;
}
</style>
