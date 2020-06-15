<template>
  <div>
    <div class="panel-title">
      Skim matrix
      <b-spinner v-if="layerState.loading" small label="Spinning"></b-spinner>
    </div>
    <b-form>
      <b-form-group label="Attribute" label-cols="3">
        <b-form-select :options="availableAttributes" v-model="layerState.requestedAttribute" :disabled="layerState.loading" />
      </b-form-group>
      <b-form-group label="Metric" label-cols="3">
        <b-form-select :options="availableMetrics" v-model="layerState.requestedMetric" :disabled="layerState.loading" />
      </b-form-group>
      <b-form-group label="" label-cols="3" v-if="!layerState.loading">
        <b-button v-on:click="startCalculation()" :disabled="layerState.metric == layerState.requestedMetric && layerState.attribute == layerState.requestedAttribute">Calculate</b-button>
      </b-form-group>
      <b-form-group label="" label-cols="3" v-if="layerState.loading">
        <b-progress :value="progress" :max="1.0" show-progress animated></b-progress>
      </b-form-group>
      <b-form-group label="Min. value" label-cols="3">
        <b-form-input v-model="layerState.minimumValue" :disabled="layerState.loading" />
      </b-form-group>
      <b-form-group label="Max. value" label-cols="3">
        <b-form-input v-model="layerState.maximumValue" :disabled="layerState.loading" />
      </b-form-group>
    </b-form>
  </div>
</template>

<script>
import * as axios from "axios";

export default {
  name: "ZoneLayerPanel",
  props: ["layerState"],
  data() {
    return {
      availableAttributes: [
        { value: "travel_time", text: "Travel time" },
        { value: "network_distance", text: "Network distance" }
      ],
      availableMetrics: [
        { value: "mean", text: "Mean" },
        { value: "median", text: "Median" },
        { value: "max", text: "Maximum" },
        { value: "min", text: "Minimum" }
      ],
      progress: 0.0,
    };
  },
  methods: {
    startCalculation() {
      this.layerState.metric = this.layerState.requestedMetric;
      this.layerState.attribute = this.layerState.requestedAttribute;

      this.layerState.loading = true;
      this.progress = 0.0;

      var self = this;
      var url = window.location.protocol + "//" + window.location.hostname + ":5000";

      var updateProgress = function() {
        axios.get(url + "/skim/status/abc").then((response) => {
            if (response.data.state == "processing") {
              self.progress = response.data.progress;
              setTimeout(updateProgress, 250);
            } else {
              self.progress = 1.0;
              self.loadData();
            }
        });
      };

      axios.get(url + "/skim/calculate/abc/" + this.layerState.attribute + "/" + this.layerState.metric).then(() => {
        updateProgress();
      });
    },
    loadData() {
      var url = window.location.protocol + "//" + window.location.hostname + ":5000";

      axios.get(url + "/skim/shape/abc").then((response) => {
        this.layerState.features = response.data.features;
        this.layerState.loading = false;
      });

      axios.get(url + "/skim/data/abc").then((response) => {
        var data = {};

        response.data.forEach((item) => {
          if (data[item["origin_municipality_id"]] == undefined) {
            data[item["origin_municipality_id"]] = {};
          }

          data[item["origin_municipality_id"]][
            item["destination_municipality_id"]
          ] = item["value"];
        });

        console.log(data);
        this.layerState.data = data;
      });
    }
  }
}
</script>
