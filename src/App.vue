<template>
  <b-container fluid style="height: 100%;">
    <b-navbar toggleable="lg" type="dark" variant="info" style="position: absolute; z-index: 100; width: 100%; margin-left:-1em;">
      <b-navbar-brand href="#">eqarun</b-navbar-brand>
      <b-navbar-nav>
        <b-nav-item href="#">Visualization</b-nav-item>
      </b-navbar-nav>
    </b-navbar>
    <b-row align-v="stretch" style="height: 100%;">
      <b-col id="panel" cols="3" style="padding-top: 60px;">
        <ZoneLayerPanel :layerState="layerState" v-if="false" />
        <RequestsLayerPanel :layerState="requestsLayerState" v-if="false" />
        <ActivitiesLayerPanel :layerState="activitiesLayerState" v-if="false" />
        <SkimMatrixLayerPanel :layerState="skimLayerState" />
      </b-col>
      <b-col>
        <svg id="map" v-on:wheel="onScale" v-on:mousedown="onMouseDown" v-on:mouseup="onMouseUp" v-on:mouseover="onMouseMove" >
          <ZoneLayer :layerState="layerState" v-if="false"  />
          <RequestsLayer :layerState="requestsLayerState" v-if="false"  />
          <ActivitiesLayer :layerState="activitiesLayerState" v-if="false" />
          <SkimMatrixLayer :layerState="skimLayerState" />
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

import ActivitiesLayerPanel from "./components/ActivitiesLayerPanel.vue"
import ActivitiesLayer from "./components/ActivitiesLayer.vue"

import SkimMatrixLayerPanel from "./components/SkimMatrixLayerPanel.vue"
import SkimMatrixLayer from "./components/SkimMatrixLayer.vue"

import * as axios from "axios";
import * as _ from "lodash";

export default {
  name: 'App',
  components: {
    ZoneLayerPanel, ZoneLayer, RequestsLayerPanel, RequestsLayer, ActivitiesLayerPanel, ActivitiesLayer,
    SkimMatrixLayerPanel, SkimMatrixLayer
  },
  data() {
    var layerState = Vue.observable({
      attribute: "age",
      metric: "mean",
      minimumValue: 0,
      maximumValue: 100,
      features: [],
      loading: false,
      scale: 0.028, offset: [0, 0]
    });

    var requestsLayerState = Vue.observable({
      time: 5.0 * 3600.0,
      loading: false,
      requests: [],
      scale: 0.028, offset: [0, 0]
    })

    var activitiesLayerState = Vue.observable({
      loading: false,
      persons: [], selectedPerson: undefined,
      scale: 0.028, offset: [0, 0]
    })

    var skimLayerState = Vue.observable({
      loading: false,
      attribute: undefined,
      metric: undefined,
      requestedAttribute: "travel_time",
      requestedMetric: "mean",
      minimumValue: 0,
      maximumValue: 3600,
      scale: 0.028, offset: [0, 0],
      features: [], data: {}
    })

    return {
      layerState: layerState, requestsLayerState: requestsLayerState, activitiesLayerState: activitiesLayerState,
      skimLayerState: skimLayerState,
      scale: 0.028, offset: [0, 0],
      mouseDownLocation: undefined
    };
  },
  mounted() {
    this.load();
    this.loadRequests();
    this.loadActivities();
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
    },
    loadActivities() {
      this.activitiesLayerState.loading = true;
      var url = window.location.protocol + "//" + window.location.hostname + ":5000";

      axios.get(
        url + "/persons").then((response) => {
          this.activitiesLayerState.persons = response.data;
          this.activitiesLayerState.loading = false;
      });
    },
    onScale(event) {
      this.scale -= 1e-3 * event.deltaY;
      this.updateScale();
    },
    updateScale: _.debounce(function() {
      this.layerState.scale = this.scale;
      this.requestsLayerState.scale = this.scale;
      this.activitiesLayerState.scale = this.scale;
    }, 100),
    onMouseDown(event) {
      this.mouseDownLocation = [event.clientX, event.clientY];
    },
    onMouseUp() {
      this.mouseDownLocation = undefined;
    },
    onMouseMove(event) {
      if (this.mouseDownLocation != undefined) {
        this.offset = [event.clientX - this.mouseDownLocation[0], event.clientY - this.mouseDownLocation[1]];
        this.updateOffset();
      }
    },
    updateOffset: _.debounce(function() {
      this.layerState.offset = this.offset;
      this.requestsLayerState.offset = this.offset;
      this.activitiesLayerState.offset = this.offset;
    }, 100),
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
