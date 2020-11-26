<template>
  <v-container fluid fill-height class="body">
    <v-card class="ma-auto" min-width="1000px" @keyup.enter="generateUUID">
      <v-toolbar color="#27303e" dark flat>
        <v-toolbar-title>UUID generator</v-toolbar-title>
      </v-toolbar>
      <v-card-text>
        <v-card-actions>
          <div class="row">
            <div class="col-2">
              <v-btn color="#27303e" class="generate-btn" @click="generateUUID">Generate</v-btn>
            </div>
            <div class="col-10">
              <span>{{ uuid }}</span>
            </div>
          </div>
        </v-card-actions>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import {GENERATE_UUID} from "@/store/actions.type";

export default {
  name: "IdGenerator",
  computed: {
    uuid() {
      return this.$store.state.uuid.uuid;
    }
  },
  data() {
    return {};
  },
  methods: {
    generateUUID() {
      this.$store.dispatch(GENERATE_UUID);
    },
  },
}
</script>

<style scoped>

</style>