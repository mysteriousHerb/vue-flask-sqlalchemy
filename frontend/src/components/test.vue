<script>
// comp.vue
import { mapGetters, mapActions} from "vuex";

export default {
  computed: {
    // mix the getters into computed with object spread operator
    ...mapGetters(["Getter1", "Getter2"])
  },
  methods: {
    ...mapActions([
      "increment", // map `this.increment()` to `this.$store.dispatch('increment')`

      // `mapActions` also supports payloads:
      "incrementBy" // map `this.incrementBy(amount)` to `this.$store.dispatch('incrementBy', amount)`
    ]),
    ...mapActions({
      add: "increment" // map `this.add()` to `this.$store.dispatch('increment')`
    })
  }
};
</Script>