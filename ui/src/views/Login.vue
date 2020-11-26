<template>
  <v-container fluid fill-height class="body">
    <v-card class="ma-auto" min-width="400px" @keyup.enter="validateCredentials()">
      <v-toolbar color="#27303e" dark flat>
        <v-toolbar-title>Login form</v-toolbar-title>
      </v-toolbar>
      <v-card-text>
        <LoginInputs ref="loginInputs" v-show="!isValid"/>
        <v-card-actions>
          <span v-show="hasError" class="red--text">{{ errorMsg }}</span>
          <v-spacer></v-spacer>
          <v-btn color="#27303e" v-show="!isValid" class="loginBtn" @click="validateCredentials">Login</v-btn>
        </v-card-actions>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import {LOGIN} from '../store/actions.type'
import LoginInputs from "@/views/components/LoginInputs";

export default {
  name: "login-page",
  data: () => ({
    isValid: false,
    hasError: false,
    errorMsg: "Bad username or password.",
    positions: [],
  }),
  components: {
    LoginInputs,
  },
  methods: {
    validateCredentials() {
      this.hasError = true;
      if (this.$refs["loginInputs"].validate()) {
        this.hasError = false;
        this.login()
      }
    },
    async login() {
      this.$store.dispatch(LOGIN, {
        username: this.$refs["loginInputs"].username,
        password: this.$refs["loginInputs"].password,
      }).then(() => {
        this.$router.push('/');
      })
    }
  },
};
</script>

<style>
</style>