<template>
  <div class="container-fluid">
    <div class="l_form">
      <h2>Login</h2>
        <form @submit.prevent="loginUser" id="LoginForm">
          <div class="form-group">
            <label for="username" class="form-label">Username:</label>
            <input id="first-field" type="text" name="username" class="form-check" required/>
          </div>

          <div class="form-group">
            <label for="password" class="form-label">Password:</label>
            <input id="second-field" type="password" name="password" class="form-check" required>
          </div>

          <br>

          <input id="btn" type="submit" value="Login">
        </form>
      </div>
    </div>
</template>

<script setup>
import { ref, onMounted  } from "vue";
    let csrf_token = ref("");
    onMounted(() => {
        getCsrfToken();
    });
    function loginUser()
    {
        let loginForm = document.getElementById("LoginForm");
        let form_data = new FormData(loginForm);
            fetch("/api/v1/auth/login", {
                method: 'POST',
                body: form_data,
                headers: 
                {
                    'X-CSRFToken': csrf_token.value
                }
            })
                .then(function (response) {
                    return response.json();
                })
                .catch(function (error) {
                    console.log(error);
                });
    }
    function getCsrfToken() 
    {
        fetch('/api/v1/csrf-token')
            .then((response) => response.json())
                .then((data) => {
                    console.log(data.csrf_token);
                    csrf_token.value = data.csrf_token;
        })
    }
</script>


<style>
    .l_form{
        width: 400px;
    }
    .container-fluid{
        display: flex;
        align-items: center;
        justify-content: center;
    }
    form{
        padding: 2em;
        box-shadow: 3px 3px 3px rgb(191, 197, 199);
        border-radius: 5px;
        border: 2px solid rgb(191, 197, 199);
        background-color: rgb(244, 242, 242);
    }
    #btn{
        width: 100%;
        height: 40px;
        border-radius: 5px;
        border: none;
        background-color: #3204b1;
        color: white;
    }
</style>
