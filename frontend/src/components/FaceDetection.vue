<template>
  <div>
    <v-container grid-list-md text-xs-center fluid>
      <v-layout align-center justify-center>
        <video
          id="video"
          ref="video"
          :width="display_size.width"
          :height="display_size.height"
          autoplay
          @play="detect_and_draw_faces"
        ></video>
        <canvas id="canvas" ref="canvas" :width="display_size.width" :height="display_size.height"></canvas>
      </v-layout>
      <v-layout align-center justify-center>
          <v-btn @click="download_face_descriptor"> download vector</v-btn>
      </v-layout>      
    </v-container>
  </div>
</template>

<script>
// useful tutorial: https://www.youtube.com/watch?v=CVClHLwv-4I&feature=youtu.be
// https://github.com/WebDevSimplified/Face-Detection-JavaScript/blob/master/script.js

import * as faceapi from "face-api.js";
import { async } from "q";
import { setTimeout, setInterval } from "timers";

export default {
  name: "FaceDetection",
  components: {},
  data: function() {
    return {
      display_size: { width: 640, height: 480 },
      detections: ""
    };
  },
  mounted: function() {
    this.load_models();
    this.call_faceapi();
    this.start_video();
  },
  methods: {
    call_faceapi: function() {
      console.log(faceapi.nets);
    },

    load_models: function() {
      Promise.all([
        // save the models to the public/models
        // faceapi.nets.ssdMobilenetv1.loadFromUri("/models"),
        faceapi.nets.tinyFaceDetector.loadFromUri("/models"),
        faceapi.nets.faceLandmark68Net.loadFromUri("/models"),
        faceapi.nets.faceRecognitionNet.loadFromUri("/models"),
        faceapi.nets.faceExpressionNet.loadFromUri("/models"),
        faceapi.nets.ageGenderNet.loadFromUri("/models")
      ]);
      console.log("done");
    },
    start_video: function() {
      navigator.getUserMedia(
        { video: {} },
        stream => (video.srcObject = stream),
        err => console.error(err)
      );
    },
    detect_and_draw_faces: function() {
      // https://michaelnthiessen.com/this-is-undefined/
      // https://stackoverflow.com/questions/47148363/when-to-use-vm-or-this-in-vue-js
      // arrow function is a pain in vue.js and this async function also seems to cause problem
      let vm = this;
      setInterval(async function() {
        //   After face detection and facial landmark prediction the face descriptors
        vm.detections = await faceapi
          .detectAllFaces(video, new faceapi.TinyFaceDetectorOptions())
          .withFaceLandmarks()
          .withFaceExpressions()
          .withAgeAndGender()
          .withFaceDescriptors()

        // calculated the size that is on our canvas size
        const resizedDetections = faceapi.resizeResults(
          vm.detections,
          vm.display_size
        );

        // clear canvas before drawing the new things to prevent cluttering
        vm.$refs.canvas
          .getContext("2d")
          .clearRect(0, 0, vm.$refs.canvas.width, vm.$refs.canvas.height);

        faceapi.draw.drawDetections(vm.$refs.canvas, resizedDetections);
        faceapi.draw.drawFaceLandmarks(vm.$refs.canvas, resizedDetections);
        faceapi.draw.drawFaceExpressions(vm.$refs.canvas, resizedDetections);

      }, 500);
    },
    download_face_descriptor: function(){
        console.log(this.detections)
        // specify which person as the algo track all the faces
        console.log(this.detections['0'].descriptor)
        this.axios({
        url: this.$API_URL + "/face_descriptor",
        method: "POST",
        data: {
          descriptor: this.detections['0'].descriptor
        }
      }).then(response => {});
    }
  }
};
</script>

<style scope>
@import url("https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css");

#video {
  /* position: absolute; */
  z-index: 1;
  pointer-events: none;
}

#canvas {
  position: absolute;
  z-index: 2;
  pointer-events: none;
}

.dropzone-custom-title {
  margin-top: 0;
  color: #00b782;
}

.subtitle {
  color: #314b5f;
}
</style>
