<template>
  <div>
    <div class="layer">
      <b>Population</b><br /><br />

      Name: {{ $store.state.iris.iris_name }}<br />

      Population: {{ $store.state.iris.population }}<br />
    </div>
  </div>
</template>

<script>
export default {
  name: 'Panel',
  data() {
    return {};
  }
}
</script>

<style scoped>

</style>
