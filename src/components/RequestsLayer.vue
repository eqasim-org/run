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
// import * as d3 from "d3";
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
    "layerState.time": _.debounce(function() { this.redraw(); }, 100),
    "layerState.scale": _.debounce(function() { this.redraw(); }, 100),
    "layerState.requests": _.debounce(function() { this.redraw(); }, 100),
    "layerState.offset": _.debounce(function() { this.redraw(); }, 100),
  },
  methods: {
    redraw() {
      var scale = this.layerState.scale;
      var width = this.width;
      var height = this.height;
      var offset = this.layerState.offset;

      var projection = function(x, y) {
        return [
          (x - 651791.0) * scale + width * 0.5 + offset[0],
          (y - 6862293.0) * scale + height * 0.5 + offset[1]
        ];
    }

      this.selectedRequests = this.layerState.requests.filter((item) => {
        return item.departure_time < this.layerState.time && item.pickup_time > this.layerState.time;
      }).map((item) => {
        var request = { id: item.id };
        var coordinates = projection(item.origin_x, item.origin_y);

        request["x"] = coordinates[0];
        request["y"] = coordinates[1];

        return request;
      });
    },
    onResize() {
      this.width = this.$el.parentNode.clientWidth;
      this.height = this.$el.parentNode.clientHeight;
      this.redraw();
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
