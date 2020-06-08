<template>
  <svg id="map">
     <g class="map"></g>
  </svg>
</template>

<script>
import * as d3 from 'd3';
import * as axios from 'axios';

export default {
  name: 'Map',
  data() {
    return {};
  },
  mounted() {
    var url = window.location.protocol + "//" + window.location.hostname + ":5000";
    var data = axios.get(url + '/network');
    var self = this;

    data.then(function(response) {
      var scale = 0.029;

      var width = self.$el.clientWidth;
      var height = self.$el.clientHeight;

      console.log(width + " " + height);

      var projection = d3.geoIdentity()
          .scale(scale)
          .translate([-651791.0 * scale + width * 0.5, -6862293.0 * scale + height * 0.5])

      var generator = d3.geoPath()
        .projection(projection);

      var u = d3.select('#map g.map')
        .selectAll('path')
        .data(response.data);

      var c = d3.color("steelblue");

      u.enter()
        .append('path')
        .attr('d', generator)
        .attr('stroke', "#cccccc")
        .attr('fill', function(d) {
          var myc = d3.color(c);
          myc.opacity = d.properties.population / 10000;
          return myc;
        })
        .on("mouseover", function(d) {
          self.$store.commit('setIris', d.properties)
          this.parentNode.appendChild(this);
          d3.select(this).attr("stroke", "red");
          d3.select(this).attr("z-index", 0);
          d3.select(this).attr("stroke-width", 2.0);
        })
        .on("mouseout", function() {
          d3.select(this).attr("stroke", "#cccccc");
          d3.select(this).attr("z-index", 100);
          d3.select(this).attr("stroke-width", 1.0);
        });
    });
  }
}
</script>

<style scoped>
#map {
  width: 100%;
  height: 100%;
}

#map path {
  stroke: black;
}
</style>
