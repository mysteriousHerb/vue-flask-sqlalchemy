<template>
  <div>
    <v-container fluid>
      <v-layout justify-center>
      </v-layout>
    </v-container>
  </div>
</template>

<script>
import Icon from "vue-awesome/components/Icon";
export default {
  name: "GenSessionID",
  components: {
        "v-fa-icon": Icon,
  },
  data: function() {
    return {
      id_length: 50
    };
  },
created() {
        window.addEventListener('beforeunload', () => {
            this.clean_up_session()
        }, false)
    },
  computed: {
    session_id () {
        // session_id should be sent to all the axios request to backend now
      return this.$store.state.session_id;
    }
  },
  mounted: function() {
    this.generate_session_id();
    this.initialise_session();
  },
  methods: {
    generate_session_id: function() {
      // https://gist.github.com/6174/6062387
      this.$store.dispatch("generate_session_id");
    },
    initialise_session: function() {
      // called on the first time launching
      this.axios({
        url: this.$API_URL + "/initialise_session",
        method: "POST",
        data: {
          session_id: this.session_id
        }
      });
    },
    clean_up_session: function() {
        console.log('removing the folder')
      // called before closing the browser
      this.axios({
        url: this.$API_URL + "/clean_up_session",
        method: "POST",
        data: {
          session_id: this.session_id
        }
      });
    },
    check_session: function() {
      // called before closing the browser
      this.axios({
        url: this.$API_URL + "/check_session",
        method: "POST",
        data: {
          session_id: this.session_id
        }
      }).then(response=>{
          console.log(response.data.session_id)
      });
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
