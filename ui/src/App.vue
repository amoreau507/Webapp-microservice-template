<template>
  <v-app>
    <v-app-bar app>
      <v-btn text @click="redirectTo('/')">Home</v-btn>
      <v-spacer></v-spacer>
      >
      <v-btn v-if="this.isLoginState()" @click="signin" text>Sign In</v-btn>
      <v-btn v-else @click="logout" text>Sign Out</v-btn>
    </v-app-bar>
    <v-main>
      <router-view/>
    </v-main>
  </v-app>
</template>

<script>

import {LOGOUT} from "@/store/actions.type";

export default {
  name: "App",
  computed: {},
  methods: {
    signin() {
      this.$router.push("Login");
    },
    logout() {
      this.$store.dispatch(LOGOUT)
      this.$router.push("Login");
    },
    redirectTo(path) {
      this.$router.push(path);
    },
    isLoginState() {
      return sessionStorage.getItem('token') === ''
    }
  }
};
</script>

<style>
html {
  overflow-y: auto !important;
  overflow-x: hidden !important;
}
</style>
