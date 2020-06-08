<template>
  <b-container fluid style="height: 100%;">
    <b-row align-v="stretch" style="height: 100%;">
      <b-col id="panel" cols="3">
        <Panel />
      </b-col>
      <b-col>
        <Map />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
import Map from './components/Map.vue'
import Panel from './components/Panel.vue'

export default {
  name: 'App',
  components: {
    Map, Panel
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
</style>
