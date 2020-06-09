<template>
  <div>
    <div class="panel-title">
      AV Requests
      <b-spinner v-if="layerState.loading" small label="Spinning"></b-spinner>
    </div>
    <b-form>
      <b-form-group label="Time" label-cols="3">
        <b-form-input id="range-1" v-model="layerState.time" type="range" min="0" max="86400" :disabled="layerState.loading"></b-form-input>
        <span>
          {{ (Math.round(layerState.time / 3600) + "").padStart(2, "0") }}:{{ (Math.round((layerState.time % 3600) / 60) + "").padStart(2, "0") }}:{{ (Math.round(layerState.time % 60) + "").padStart(2, "0") }}
        </span>
      </b-form-group>
    </b-form>
  </div>
</template>

<script>
export default {
  name: "RequestsLayerPanel",
  props: ["layerState"]
}
</script>
