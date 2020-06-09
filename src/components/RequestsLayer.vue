<template>
  <g class="layer">
    <circle
      v-for="request in selectedRequests"
      v-bind:key="request.id"
      v-bind:cx="request.x"
      v-bind:cy="request.y"
      r="4"
      stroke="white" stroke-width="1" fill="red"
      />
  </g>
</template>

<script>
import * as d3 from "d3";
import * as _ from "lodash";

export default {
  name: "RequestsLayer",
  data() {
    return {
      width: 0, height: 0,
      selectedRequests: []
    };
  },
  props: ["layerState"],
  watch: {
    "layerState.time": _.debounce(function() {
      var scale = 0.028;

      var projection = d3.geoIdentity()
          .scale(scale)
          .translate([-651791.0 * scale + this.width * 0.5, -6862293.0 * scale + this.height * 0.5])

      this.selectedRequests = this.layerState.requests.filter((item) => {
        return item.departure_time < this.layerState.time && item.pickup_time > this.layerState.time;
      }).map((item) => {
        var request = { id: item.id };
        var coordinates = projection([ item.origin_x, item.origin_y ]);

        request["x"] = coordinates[0];
        request["y"] = coordinates[1];

        return request;
      });
    }, 100)
  },
  methods: {
    onResize() {
      this.width = this.$el.parentNode.clientWidth;
      this.height = this.$el.parentNode.clientHeight;
    }
  },
  mounted() {
    this.onResize();
    window.addEventListener('resize', this.onResize);
  }
}
</script>

<style scoped>
</style>
