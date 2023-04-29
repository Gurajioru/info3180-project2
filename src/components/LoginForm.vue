<template>
  <div>
    <h2>Login</h2>
    <form @submit.prevent="loginUser">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" name="username" v-model="data.username" required>
      </div>
      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" name="password" v-model="data.password" required>
      </div>
      <button type="submit">Login</button>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue';

const data = reactive({
  username: '',
  password: ''
});

const csrf_token = ref('');

onMounted(() => {
  getCsrfToken();
});

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then(response => response.json())
    .then(data => {
      csrf_token.value = data.csrf_token;
    })
    .catch(error => {
      console.error('Error:', error);
      // display an error message to the user
    });
}

const loginUser = () => {
  fetch('/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf_token.value
      },
      body: JSON.stringify({
        username: data.username,
        password: data.password
      })
    })
    .then(response => response.json())
    .then(data => {
      // handle the response data
    })
    .catch(error => {
      console.error('Error:', error);
      // display an error message to the user
    });
};
</script>