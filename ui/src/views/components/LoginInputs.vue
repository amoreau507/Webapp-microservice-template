<template>
  <v-form ref="form" lazy-validation>
    <v-text-field v-model="username" :rules="usernameRules" label="Username" required outlined></v-text-field>
    <v-text-field
        v-model="password"
        :rules="passwordRules"
        label="Password"
        type="password"
        required
        outlined
    ></v-text-field>
  </v-form>
</template>

<script>
export default {
  name: "login-inputs",
  data() {
    return {
      username: "",
      usernameRules: [(v) => !!v || "Username is required"],
      password: "",
      passwordRules: [(v) => !!v || "Password is required"],
    };
  },
  methods: {
    validate() {
      return this.$refs.form.validate();
    },
  },
};
</script>

<style>
</style>