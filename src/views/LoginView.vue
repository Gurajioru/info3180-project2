<template>
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8">
          <h1>Login</h1>
          <Login />
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import Login from "../components/Login.vue";
  
  export default {
    name: "Login",
    components: { Login }
  };
  </script>