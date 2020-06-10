<template>
  <g class="layer">
    <circle
      v-for="person in selectedPersons"
      v-bind:key="person.id"
      v-bind:cx="person.x"
      v-bind:cy="person.y"
      r="4"
      stroke="white" stroke-width="1" fill="rgba(255, 0, 0, 0.1)"
      v-on:mouseenter="selectPerson(person)"
      />
    <circle
      v-if="layerState.selectedPerson"
      v-bind:cx="layerState.selectedPerson.x"
      v-bind:cy="layerState.selectedPerson.y"
      r="8"
      stroke="white" stroke-width="1" fill="rgba(255, 0, 0, 1.0)"
      />
    <g v-if="selectedActivities">
    <circle
      v-for="point in selectedActivities.points"
      v-bind:key="point.index"
      v-bind:cx="point.x"
      v-bind:cy="point.y"
      r="4"
      stroke="white" stroke-width="1" fill="rgb(255, 0, 0)"
      />
    </g>
    <path
      v-if="selectedActivities"
      v-bind:d="selectedActivities.geometry"
      stroke="red" stroke-width="2" fill="none" />
  </g>
</template>

<script>
// import * as d3 from "d3";
import * as _ from "lodash";
import * as axios from "axios";
import * as d3 from "d3";

export default {
  name: "ActivitiesLayer",
  data() {
    return {
      width: 0, height: 0,
      selectedPersons: [],
      selectedActivities: []
    };
  },
  props: ["layerState"],
  watch: {
    "layerState.scale": _.debounce(function() { this.redraw(); }, 100),
    "layerState.persons": _.debounce(function() {
      var self = this;

      this.layerState.persons.forEach(function(person) {
          if (person.id == "8902471") {
            self.selectPerson(person);
          }
      });

      this.redraw();
    }, 100),
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

      this.selectedPersons = this.layerState.persons.map((item) => {
        var person = { id: item.id };
        var coordinates = projection(item.x, item.y);

        person["x"] = coordinates[0];
        person["y"] = coordinates[1];

        return person;
      });
    },
    onResize() {
      this.width = this.$el.parentNode.clientWidth;
      this.height = this.$el.parentNode.clientHeight;
      this.redraw();
    },
    selectPerson: _.debounce(function(person) {
      this.layerState.selectedPerson = person;
      var url = window.location.protocol + "//" + window.location.hostname + ":5000";

      axios.get(
        url + "/activities/" + person.id).then((response) => {
          var scale = this.layerState.scale;
          var width = this.width;
          var height = this.height;
          var offset = this.layerState.offset;

          var line = d3.line()
            .x(function(d) { return (d.x - 651791.0) * scale + width * 0.5 + offset[0]; })
            .y(function(d) { return (d.y - 6862293.0) * scale + height * 0.5 + offset[1]; });

          var points = response.data.map(function(item) {
            return {
              x: (item.x - 651791.0) * scale + width * 0.5 + offset[0],
              y: (item.y - 6862293.0) * scale + height * 0.5 + offset[1],
            };
          });

          var selectedActivities = response.data;
          selectedActivities.geometry = line(selectedActivities);
          selectedActivities.points = points;
          this.selectedActivities = selectedActivities;
      });
    }, 100)
  },
  mounted() {
    this.onResize();
    window.addEventListener('resize', this.onResize);
  }
}
</script>

<style scoped>
</style>
