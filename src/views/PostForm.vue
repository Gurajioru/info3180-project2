<template>
    <form id="PostForm" @submit.prevent="savePost">
        <div class = "form-group mb-3">
            <label for="image">Poster</label>
            <input type="file" class="form-control-file" id="image/"/>
            <label for="title" class="form-label">Caption</label>
            <input type="text" name="description" class="form-control"/>
            <input type="hidden" name="csrf_token" :value="csrf_token" />
            <button type="Submit">Submit</button>
        </div>
    </form>
</template>

<script setup>
     
    function savePost(){

        fetch("api/v1/users/<user_id>/posts",{
            method:'POST'
        })
            .then(function (response) {
                return response.json();
            })
            .then(function (data) {
                flash('Succesful')
                console.log(data)
            })
            .catch(function (error) {
                console.log(error);
            })
    }

</script>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      userId: null,
      name: null,
      iat: null
    };
  },
  mounted() {
    // Make a request to the Flask backend to obtain the JWT token
    axios.get('/api/get_token')
      .then(response => {
        const jwt = response.data.token;
        // Split the JWT into its parts: header, payload, signature
        const parts = jwt.split('.');
        const encodedPayload = parts[1];

        // Decode the base64Url encoded payload
        const decodedPayload = atob(encodedPayload);

        // Parse the JSON representation of the payload
        const payload = JSON.parse(decodedPayload);

        // Access the desired payload data and set it to Vue component's data properties
        this.userId = payload.sub;
        this.name = payload.name;
        this.iat = payload.iat;
      })
      .catch(error => {
        console.error('Error obtaining JWT token: ', error);
      });
  }
};
</script>