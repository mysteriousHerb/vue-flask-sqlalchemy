<template>
  <div id="app">
    <v-app>
      <!-- drawer is the section popup from the left-->
      <v-navigation-drawer fixed v-model="drawer" app>
        <v-list dense>
          <!-- use a v-for to automatically generate  -->
          <li v-for="route in routes" :key="route.id">
            <v-list-tile @click="change_view(route.name)">
              <v-list-tile-action>
                <v-icon>{{route.icon}}</v-icon>
              </v-list-tile-action>
              <v-list-tile-content>
                <v-list-tile-title>{{route.name}}</v-list-tile-title>
              </v-list-tile-content>
            </v-list-tile>
          </li>
        </v-list>
      </v-navigation-drawer>

      <!-- v-toolbar refer to the horizontal bar at the top-->
      <v-toolbar color="#41B883" dark fixed app>
        <v-toolbar-title left>Application</v-toolbar-title>
        <v-toolbar-side-icon @click.stop="drawer = !drawer" left></v-toolbar-side-icon>
      </v-toolbar>

      <v-content>
        <v-container>
          <!--this doesnt really have a view component -->
          <GenSessionID/>
          <router-view/>
        </v-container>
      </v-content>

      <v-bottom-nav :active.sync="current_view" :value="true" absolute color="transparent">
        <div v-for="route in EnabledRoutes" :key="route.name" class="display-2">
          <div v-if="route.enabled">
            <v-btn color="teal" flat :value="route.name" @click="change_view(route.name)">
              <span>{{route.name}}</span>
              <v-fa-icon :name="route.icon" scale="2"/>
            </v-btn>
          </div>
        </div>
      </v-bottom-nav>
    </v-app>
  </div>
</template>

<script>
import Icon from "vue-awesome/components/Icon";
import GenSessionID from "@/components/GenSessionID.vue";

export default {
  components: {
    "v-fa-icon": Icon,
    GenSessionID
  },
  data: function() {
    return {
      drawer: false,
      routes: [
        { name: "Home", address: "/", icon: "home", enabled: false },
        { name: "About", address: "/about", icon: "search", enabled: false },
        { name: "Todo", address: "/todo", icon: "edit", enabled: false },
        { name: "UploadSmithKey", address: "/upload_key", icon: "key", enabled: true },
        {
          name: "FaceRecognition",
          address: "/face",
          icon: "smile",
          enabled: false
        },
        {
          name: "GenSmithKey",
          address: "/gen_key",
          icon: "save",
          enabled: true
        }
      ],
      current_view: "UploadSmithKey"
    };
  },
  computed: {
    EnabledRoutes: function() {
      return this.routes.filter(function(route) {
        return route.enabled;
      });
    },
    user_name_in_key(){
      return this.$store.state.user_name_in_key;
    },
  },
  watch: {
    // whenever supplied with a key, then change_view
    user_name_in_key(){
      this.change_view('FaceRecognition')
    }
  },
  mounted: function() {
    this.change_view(this.current_view);
  },
  methods: {
    change_view: function(view) {
      console.log(view);
      this.$router.push({ name: view });
      this.current_view = view;
    }
  }
};
</script>


<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
#nav {
  padding: 30px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #42b983;
}
</style>
