<template>
  <b-container fluid style="height: 100%;">
    <b-row align-v="stretch" style="height: 100%;">
      <b-col id="panel" cols="3">
        <ZoneLayerPanel :layerState="layerState" />
      </b-col>
      <b-col>
        <svg id="map">
          <ZoneLayer :layerState="layerState"  />
        </svg>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import Vue from 'vue'

import ZoneLayerPanel from "./components/ZoneLayerPanel.vue"
import ZoneLayer from "./components/ZoneLayer.vue"

import * as axios from "axios";

export default {
  name: 'App',
  components: {
    ZoneLayerPanel, ZoneLayer
  },
  data() {
    var layerState = Vue.observable({
      attribute: "age",
      metric: "mean",
      minimumValue: 0,
      maximumValue: 100,
      features: [],
      loading: false
    });

    return { layerState: layerState };
  },
  mounted() {
    this.load();
  },
  methods: {
    load() {
      this.layerState.loading = true;
      var url = window.location.protocol + "//" + window.location.hostname + ":5000";

      axios.get(
        url + "/population/" + this.layerState.attribute + "/" + this.layerState.metric).then((response) => {
          this.layerState.features = response.data.features;
          this.layerState.minimumValue = response.data.minimumValue;
          this.layerState.maximumValue = response.data.maximumValue;
          this.layerState.loading = false;
      });
    }
  },
  watch: {
    "layerState.metric": function() { this.load() },
    "layerState.attribute": function() { this.load() }
  }
}
</script>

<style>
html,body {
  height: 100%;
  margin: 0;
}

#panel {
  background-color: rgb(240, 240, 240);
}

#map {
  width: 100%;
  height: 100%;
}

.panel-title {
  font-weight: bold;
  padding-bottom: 1em;
  padding-top: 1em;
}
</style>
