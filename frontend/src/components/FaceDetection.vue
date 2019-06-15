<template>
  <div>
    <v-container grid-list-md text-xs-center fluid>
      <v-layout justify-center>
        <label>Instruction: {{current_instruction}}</label>
      </v-layout>
      <v-layout justify-center>
        <video
          id="video"
          ref="video"
          :width="display_size.width"
          :height="display_size.height"
          :top="display_location.top"
          :left="display_location.left"
          style="position: absolute;"
          autoplay
          @play="detect_and_draw_faces"
        ></video>

        <canvas
          id="canvas_flip"
          ref="canvas_flip"
          :width="display_size.width"
          :height="display_size.height"
          :top="display_location.top"
          :left="display_location.left"
          style="transform: scaleX(-1);"
        ></canvas>

        <canvas
          id="canvas"
          ref="canvas"
          :width="display_size.width"
          :height="display_size.height"
          :top="display_location.top"
          :left="display_location.left"
        ></canvas>
      </v-layout>
      <v-layout align-center justify-center>
        <v-btn @click="download_face_descriptor">download vector</v-btn>
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
import FileSaver from "file-saver";
import { exists } from "fs";
import { shuffle } from "@tensorflow/tfjs-core/dist/util";

export default {
  name: "FaceDetection",
  components: {},
  data: function() {
    return {
      display_size: { width: 640, height: 480 },
      display_location: { top: 500, left: 50 },
      detections: [],
      resizedDetections: [],
      refresh_time: 50,
      // determine sensitivity for left and right face, higher = more turning needed
      left_right_turning_ratio: 1.5,
      // determine sensitivity for look up, higher = more turning needed
      up_slope_threshold: -0.1,
      // larger the more opening
      mouth_threshold: 0.6,
      // larger the more opening
      eyebrow_threshold: 1.0,
      // List of available instructions
      instructions: [
        "Turn Left!",
        "Turn Right!",
        "Look Up!",
        "Smile!",
        "Open mouth!",
        "Raise eyebrows!"
      ],
      current_instruction: "",
      liveness_detection_status: {
        left_right_status: "neutral",
        up_down_status: "neutral",
        expression: "neutral",
        mouth: "neutral",
        eyebrow: "neutral"
      },
      liveness_test_instructions: []
    };
  },
  mounted: function() {
    this.load_models();
    this.start_video();
    this.generate_liveness_test();
  },
  computed: function(){

  },
  methods: {
    generate_liveness_test: function() {
      // DEBUG: add a timer for each test?
      function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
          const j = Math.floor(Math.random() * (i + 1));
          [array[i], array[j]] = [array[j], array[i]];
        }
      }
      if (this.instructions.length == 0){
        alert('you are a human')
        this.current_instruction = 'do some humanitarian things!'
      }
      else{
      shuffleArray(this.instructions);
      this.current_instruction = this.instructions[0];}
    },
    liveness_test:function(){
      var test = this.current_instruction
      var result = this.liveness_detection_status
      if (test == 'Turn Left!' && result.left_right_status =='left')
      {return true}
      else if (test == 'Turn Right!' && result.left_right_status =='right')
      {return true}
            else if (test == 'Look Up!' && result.up_down_status =='up')
      {return true}
          else if (test == 'Smile!' && result.expression =='happy')
      {return true}
                else if (test == 'Open mouth!' && result.mouth =='open')
      {return true}
                      else if (test == 'Raise eyebrows!' && result.eyebrow =='raised')
      {return true}
    },
  
    load_models: function() {
      // save the models to the public/models
      // faceapi.nets.ssdMobilenetv1.loadFromUri("/models"),
      Promise.all([
        faceapi.nets.tinyFaceDetector.loadFromUri("/models"),
        faceapi.nets.faceLandmark68Net.loadFromUri("/models"),
        faceapi.nets.faceRecognitionNet.loadFromUri("/models"),
        faceapi.nets.faceExpressionNet.loadFromUri("/models")
      ]).then(console.log("model loaded"));
    },
    start_video: function() {
      navigator.getUserMedia(
        { video: {} },
        stream => (video.srcObject = stream),
        err => console.error(err)
      );
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
          .withFaceLandmarks()
          .withFaceExpressions();
        // calculating the 128 descriptors seems to be rather slow, lets not do it very frequent or do it in backend
        // .withFaceDescriptors();

        if (self.detections) {
          // calculated the size that is on our canvas size
          const resizedDetections = faceapi.resizeResults(
            self.detections,
            self.display_size
          );

          // replace the result with scaled one, all the other information will remain
          self.detections = resizedDetections;

          // call other methods
          self.mouth_eye_status();
          self.head_pose_estimation();
          self.find_expression();

          // annotation
          var message2 = [
            "L/R: " + self.liveness_detection_status.left_right_status,
            "U/D: " + self.liveness_detection_status.up_down_status,
            "Expression: " + self.liveness_detection_status.expression,
            "mouth: " + self.liveness_detection_status.mouth,
            "eyebrow: " + self.liveness_detection_status.eyebrow
          ];
          self.annotation({
            clear: false,
            message: "HELLO",
            message2: message2
          });

          // liveness test is passed, we move on with next test
          if (self.instructions.length != 0){
          if (self.liveness_test()){
              self.instructions.shift()
              self.generate_liveness_test()
              console.log('Passed one test, now move on!')
          }
          }

        } else {
          self.annotation({ clear: true });
        }
      }, self.refresh_time);
    },
    // note how to use named arguments in javascript...
    annotation: function({ clear = false, message = "Hello!", message2 = [] }) {
      var canvas = this.$refs.canvas;
      var canvas_flip = this.$refs.canvas_flip;

      // clear canvas before drawing the new things to prevent cluttering
      canvas.getContext("2d").clearRect(0, 0, canvas.width, canvas.height);
      canvas_flip
        .getContext("2d")
        .clearRect(0, 0, canvas_flip.width, canvas_flip.height);

      // set to clear when no face can be found
      if (clear === false) {
        // NOTE: There are some useful drawing functions already exist
        faceapi.draw.drawFaceLandmarks(canvas_flip, this.detections);

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
        const boxOptions = {
          label: message,
          lineWidth: 2,
          boxColor: "rgba(57,255,20,0.8)"
        };
        // flip the x-value x, y, width, height
        const drawBox = new faceapi.draw.DrawBox(box_X_flipped, boxOptions);
        drawBox.draw(canvas);

        // ------- multi-line text at bottom -------
        if (message2.length != 0) {
          const text = message2;
          const anchor = this.detections.detection.box.bottomLeft;
          const anchor_X_flipped = {
            x: canvas.width - anchor.x - box.width,
            y: anchor.y
          };
          // see DrawTextField below
          const textOptions = {
            anchorPosition: "TOP_LEFT",
            backgroundColor: "rgba(57,255,20, 0.5)"
          };
          const drawText = new faceapi.draw.DrawTextField(
            text,
            anchor_X_flipped,
            textOptions
          );
          drawText.draw(canvas);
        }
      }
    },
    find_expression: function() {
      var expressions = this.detections.expressions;
      // find the max value of all the keys
      // The reducer function takes four arguments: Accumulator (acc), Current Value (cur), Current Index (idx)
      // the question mark is conditional operator, which returns true_val:false_val
      var likely_expression = Object.keys(expressions).reduce((i, j) =>
        expressions[i] > expressions[j] ? i : j
      );
      var expression_possibility = expressions[likely_expression];
      this.liveness_detection_status["expression"] = likely_expression;

      return likely_expression + ":" + String(expression_possibility);
    },
    head_pose_estimation: function() {
      const landmarks = this.detections.landmarks;
      const landmarkPositions = landmarks.positions;

      // the distance between 1 and 28 will be shorter when extending left face
      const right_face_distance = faceapi.euclideanDistance(
        Object.values(landmarkPositions[16]),
        Object.values(landmarkPositions[28])
      );
      const left_face_distance = faceapi.euclideanDistance(
        Object.values(landmarkPositions[0]),
        Object.values(landmarkPositions[28])
      );
      const right_to_left_face_ratio = right_face_distance / left_face_distance;

      // the point 6 - 12 become more flat when facing upward. calculate the slope
      const chin_slope_left =
        (landmarkPositions[5].y - landmarkPositions[8].y) /
        (landmarkPositions[8].x - landmarkPositions[5].x);
      const chin_slope_right =
        (landmarkPositions[11].y - landmarkPositions[8].y) /
        (landmarkPositions[11].x - landmarkPositions[8].x);
      const chin_slope_average = (chin_slope_left + chin_slope_right) / 2;
      // NOTE: make this vue variable

      if (
        right_to_left_face_ratio > 1 / this.left_right_turning_ratio &&
        right_to_left_face_ratio < this.left_right_turning_ratio
      ) {
        this.liveness_detection_status["left_right_status"] = "neutral";
      } else if (right_to_left_face_ratio > this.left_right_turning_ratio) {
        this.liveness_detection_status["left_right_status"] = "right";
      } else if (right_to_left_face_ratio < 1 / this.left_right_turning_ratio) {
        this.liveness_detection_status["left_right_status"] = "left";
      }
      if (chin_slope_average > this.up_slope_threshold) {
        this.liveness_detection_status["up_down_status"] = "up";
      } else {
        this.liveness_detection_status["up_down_status"] = "neutral";
      }
    },
    mouth_eye_status: function() {
      //  https://towardsdatascience.com/mouse-control-facial-movements-hci-app-c16b0494a971
      var landmarks = this.detections.landmarks;
      const landmarkPositions = landmarks.positions;
      // https://www.pyimagesearch.com/2017/04/24/eye-blink-detection-opencv-python-dlib/
      const mouth_y = faceapi.euclideanDistance(
        Object.values(landmarkPositions[51]),
        Object.values(landmarkPositions[57])
      );
      const mouth_x = faceapi.euclideanDistance(
        Object.values(landmarkPositions[54]),
        Object.values(landmarkPositions[48])
      );
      const mouth_aspect_ratio = mouth_y / mouth_x;
      if (mouth_aspect_ratio > this.mouth_threshold){
        this.liveness_detection_status.mouth = 'open'
      }
      else {
        this.liveness_detection_status.mouth = 'neutral'
      }

      //  ------------- eyebrow measurment: use the distance between eyebrow and eye vs 
      // the width of the eyes (rather constant)  to test whether the eyebrows are raised
      const l_eyebrow_eye_d = faceapi.euclideanDistance(
        Object.values(landmarkPositions[19]),
        Object.values(landmarkPositions[37])
      );
      const r_eyebrow_eye_d = faceapi.euclideanDistance(
        Object.values(landmarkPositions[24]),
        Object.values(landmarkPositions[44])
      );
      // use eyebrow as a reference point
      const l_eye_w = faceapi.euclideanDistance(
        Object.values(landmarkPositions[39]),
        Object.values(landmarkPositions[36])
      );
      const r_eye_w = faceapi.euclideanDistance(
        Object.values(landmarkPositions[42]),
        Object.values(landmarkPositions[45])
      );
      const eyebrow_d_eye_w_ratio =
        (l_eyebrow_eye_d + r_eyebrow_eye_d) / (l_eye_w + r_eye_w);

      if (eyebrow_d_eye_w_ratio > this.eyebrow_threshold){
        this.liveness_detection_status.eyebrow = 'raised'
      }
      else {
        this.liveness_detection_status.eyebrow = 'neutral'
      }

    },
    download_face_descriptor: function() {
      console.log(this.detections);
      var detections_json = JSON.stringify(this.detections);
      var blob = new Blob([detections_json], { type: "application/json" });
      FileSaver.saveAs(blob, "key.json");
    },
    communicate_face_descriptor: function() {
      console.log(this.detections);
      // specify which person as the algo track all the faces
      console.log(this.detections["0"].descriptor);
      this.axios({
        url: this.$API_URL + "/face_descriptor",
        method: "POST",
        data: {
          descriptor: this.detections["0"].descriptor
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
  pointer-events: none;
  /* flip the image so it is more natural */
  transform: scaleX(-1);
}

#canvas {
  position: absolute;
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
