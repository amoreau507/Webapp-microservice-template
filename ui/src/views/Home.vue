<template>
  <v-container fluid fill-height class="body">
    <div class="d-flex flex-column ma-auto">
      <IdGenerator></IdGenerator>
    </div>
  </v-container>
</template>

<script>
import IdGenerator from "./components/IdGenerator";

export default {
  name: "home-page",
  components: {
    IdGenerator
  },
  computed: {},
  data() {
  }
};
</script>

<style>
</style>