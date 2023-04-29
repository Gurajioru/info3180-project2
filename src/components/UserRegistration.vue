<template>
  <form @submit.prevent="saveEntry" id="RegistrationForm" enctype="multipart/form-data" method="post">
    <div class="form-group mb-3">
      <label for="username" class="form-label">Username</label>
      <input type="username" name="username" v-model="username" class="form-control" />
    </div>
    <div class="form-group mb-3">
      <label for="password" class="form-label">Password</label>
      <input type="password" name="password" v-model="password" class="form-control" />
    </div>
    <div class="form-group mb-3">
      <label for="first-name" class="form-label">First Name</label>
      <input type="text" name="first-name" v-model="firstName" class="form-control" />
    </div>
    <div class="form-group mb-3">
      <label for="last-name" class="form-label">Last Name</label>
      <input type="text" name="last-name" v-model="lastName" class="form-control" />
    </div>
    <div class="form-group mb-3">
      <label for="email" class="form-label">Email</label>
      <input type="text" name="email" v-model="email" class="form-control" />
    </div>
    <div class="form-group mb-3">
      <label for="location" class="form-label">Location</label>
      <input type="text" name="location" v-model="location" class="form-control" />
    </div>
    <div class="form-group mb-3">
      <label for="biography" class="form-label">Biography</label>
      <textarea name="biography" v-model="biography" class="form-control"></textarea>
    </div>
    <div class="form-group mb-3">
      <label for="photo" class="form-label">Photo</label>
      <input type="file" name="photo" ref="photoInput" class="form-control" @change="onPhotoChange"/>
    </div>
    <div class="form-group mb-3">
      <img :src="photoUrl" class="img-thumbnail" v-if="photoUrl" />
    </div>
    <button type="submit" class="btn btn-primary">Register</button>
  </form>
</template>

<script setup>
  import { ref } from 'vue';

  const firstName = ref('');
  const lastName = ref('');
  const username = ref('');
  const password = ref('');
  const email = ref('');
  const location = ref('');
  const biography = ref('');
  const photoUrl = ref('');

  const onPhotoChange = () => {
    const file = event.target.files[0];
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      photoUrl.value = reader.result;
    };
  };

  const saveEntry = () => {
    const formData = new FormData();
    formData.append('username', username.value);
    formData.append('password', password.value);
    formData.append('firstName', firstName.value);
    formData.append('lastName', lastName.value);
    formData.append('email', email.value);
    formData.append('location', location.value);
    formData.append('biography', biography.value);
    formData.append('photo', refs.photoInput.files[0]);

    fetch('api/v1/register', {
      method: 'POST',
      body: formData,
    })
      .then(response => {
        if (response.ok) {
          return response.json();
        } else {
          throw new Error('Failed to register');
        }
      })
      .then(data => {
        console.log(data);
        // do something with the response data
      })
      .catch(error => {
        console.error(error);
      });
  };
</script>