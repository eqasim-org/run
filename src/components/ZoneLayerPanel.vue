<template>
  <div>
    <div class="panel-title">
      Population by zone
      <b-spinner v-if="layerState.loading" small label="Spinning"></b-spinner>
    </div>
    <b-form>
      <b-form-group label="Attribute" label-cols="3">
        <b-form-select :options="availableAttributes" v-model="layerState.attribute" :disabled="layerState.loading" />
      </b-form-group>
      <b-form-group label="Metric" label-cols="3">
        <b-form-select :options="availableMetrics" v-model="layerState.metric" :disabled="layerState.loading" />
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
export default {
  name: "ZoneLayerPanel",
  props: ["layerState"],
  data() {
    return {
      availableAttributes: [
        { value: "age", text: "Age" },
        { value: "income", text: "Income" },
        { value: "commute_distance", text: "Commute distance" }
      ],
      availableMetrics: [
        { value: "mean", text: "Mean" },
        { value: "median", text: "Median" },
        { value: "q10", text: "10% Quantile" },
        { value: "q90", text: "90% Quantile" },
        { value: "gini", text: "Gini Coefficient" },
        { value: "max", text: "Maximum" },
        { value: "min", text: "Minimum" }
      ],
    };
  }
}
</script>
