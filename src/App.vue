<template>
  <b-container fluid style="height: 100%;">
    <b-row align-v="stretch" style="height: 100%;">
      <b-col id="panel" cols="3">
        <ZoneLayerPanel :layerState="layerState" />
        <RequestsLayerPanel :layerState="requestsLayerState" />
      </b-col>
      <b-col>
        <svg id="map">
          <ZoneLayer :layerState="layerState"  />
          <RequestsLayer :layerState="requestsLayerState"  />
        </svg>
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import Vue from 'vue'

import ZoneLayerPanel from "./components/ZoneLayerPanel.vue"
import ZoneLayer from "./components/ZoneLayer.vue"

import RequestsLayerPanel from "./components/RequestsLayerPanel.vue"
import RequestsLayer from "./components/RequestsLayer.vue"

import * as axios from "axios";

export default {
  name: 'App',
  components: {
    ZoneLayerPanel, ZoneLayer, RequestsLayerPanel, RequestsLayer
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

    var requestsLayerState = Vue.observable({
      time: 5.0 * 3600.0,
      loading: false,
      requests: [],
    })

    return { layerState: layerState, requestsLayerState: requestsLayerState };
  },
  mounted() {
    this.load();
    this.loadRequests();
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
    },
    loadRequests() {
      this.requestsLayerState.loading = true;
      var url = window.location.protocol + "//" + window.location.hostname + ":5000";

      axios.get(
        url + "/requests").then((response) => {
          this.requestsLayerState.requests = response.data;
          this.requestsLayerState.loading = false;
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
