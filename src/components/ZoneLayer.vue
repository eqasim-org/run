<template>
  <g class="layer">
    <path
      v-for="zone in zones"
      v-bind:key="zone.id"
      v-bind:d="zone.geometry"
      v-on:mouseenter="onEnter(zone)"
      v-on:mouseleave="onLeave(zone)"
      v-bind:style="{ fill: zone.color }"
      />
  </g>
</template>

<script>
import * as d3 from "d3";

export default {
  name: "ZoneLayer",
  data() {
    return {
      hoverZone: undefined,
      width: 0, height: 0
    };
  },
  props: ["layerState"],
  computed: {
    zones() {
      var scale = this.layerState.scale;
      var width = this.width;
      var height = this.height;
      var offset = this.layerState.offset;

      var projection = d3.geoTransform({
        point: function(x, y) {
          this.stream.point(
            (x - 651791.0) * scale + width * 0.5 + offset[0],
            (y - 6862293.0) * scale + height * 0.5 + offset[1]
          );
        }
      });

      var generator = d3.geoPath()
        .projection(projection);

      var baseColor = d3.color("steelblue");

      return this.layerState.features.map((item) => {
        var color = d3.color(baseColor);
        color.opacity = (item.properties.value - this.layerState.minimumValue) / (this.layerState.maximumValue - this.layerState.minimumValue)

        return { id: item.properties.iris_id, color: color, geometry: generator(item) };
      });
    }
  },
  methods: {
    onEnter(zone) {
      this.hoverZone = zone;
      event.target.parentNode.appendChild(event.target);
      event.target.classList.add("hover")
      this.$emit("hoverZone", zone);
    },
    onLeave() {
      this.hoverZone = undefined;
      event.target.classList.remove("hover")
      this.$emit("hoverZone", undefined);
    },
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
path {
  stroke: #cccccc;
  fill: white;
}

path.hover {
  stroke: red;
}
</style>
