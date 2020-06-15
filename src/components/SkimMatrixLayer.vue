<template>
  <g class="layer">
    <path
      v-for="zone in zones"
      v-bind:key="zone.id"
      v-bind:d="zone.geometry"
      v-on:mouseenter="onEnter(zone)"
      v-on:mouseleave="onLeave(zone)"
      v-on:click="onClick(zone)"
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
      hoverZone: undefined, clickZone: undefined,
      width: 0, height: 0,
      hoverSelectedMunicipalityId: undefined,
      clickSelectedMunicipalityId: undefined
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

      var selectedMunicipalityId = this.hoverSelectedMunicipalityId;

      if (selectedMunicipalityId == undefined) {
        selectedMunicipalityId = this.clickSelectedMunicipalityId;
      }

      return this.layerState.features.map((item) => {
        var color = d3.color(baseColor);
        color.opacity = 0.0;

        if (selectedMunicipalityId != undefined) {
          var selectedValues = this.layerState.data[selectedMunicipalityId];

          if (selectedValues != undefined) {
            var value = selectedValues[item.properties.municipality_id];

            if (value != undefined) {
              color.opacity = (value - this.layerState.minimumValue) / (this.layerState.maximumValue - this.layerState.minimumValue)
            }
          }
        }

        /*color.opacity = (item.properties.value - this.layerState.minimumValue) / (this.layerState.maximumValue - this.layerState.minimumValue)
        color.opacity = 0.0;*/

        return { id: item.properties.municipality_id, color: color, geometry: generator(item) };
      });
    }
  },
  methods: {
    onClick(zone) {
      if (this.clickedElement != undefined) {
        this.clickedElement.classList.remove("selected");
      }

      this.clickSelectedMunicipalityId = zone.id;
      this.clickedElement = event.target;
      this.clickedElement.classList.add("selected");
    },
    onEnter(zone) {
      this.hoverSelectedMunicipalityId = zone.id;
      this.hoverZone = zone;
      event.target.parentNode.appendChild(event.target);
      event.target.classList.add("hover")
      this.$emit("hoverZone", zone);

      if (this.clickedElement != undefined) {
        this.clickedElement.parentNode.appendChild(this.clickedElement);
      }
    },
    onLeave() {
      this.hoverSelectedMunicipalityId = undefined;
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

path.selected {
  stroke: blue;
  stroke-width: 2;
}

path.hover {
  stroke: red;
}
</style>
