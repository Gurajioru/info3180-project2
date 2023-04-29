<template>
  <div class="container-fluid">
    <div class="reg_form">
        <h3>Register</h3>
        <form @submit.prevent="saveEntry" id="RegistrationForm">
            <div class="entry">
                <label for="username" class="form-label">Username</label>
                <input id="first-field" type="text" name="username" class="form-check" />
            </div>

            <br>

            <div class="entry">
                <label for="password" class="form-label">Password</label>
                <input id="second-field" type="password" name="password" class="form-check" />
            </div>

            <br>

            <div class="entry">
                <label for="firstname" class="form-label">Firstname</label>
                <input id="third-field" type="text" name="firstname" class="form-check" />
            </div>

            <br>

            <div class="entry">
                <label for="lastname" class="form-label">Lastname</label>
                <input id="fourth-field" type="text" name="lastname" class="form-check" />
            </div>

            <br>

            <div class="entry">
                <label for="email" class="form-label">Email</label>
                <input id="fifth-field" type="text" name="email" class="form-check" />
            </div>

            <br>

            <div class="entry">
                <label for="location" class="form-label">Location</label>
                <input id="sixth-field" type="text" name="location" class="form-check" />
            </div>

            <br>

            <div class="entry">
                <label for="biography" class="form-label">Biography</label>
                <input id="seventh-field" type="text" name="biography" class="form-check" />
            </div>

            <br>

            <div class="entry">
                <label for="photo" class="form-label">Photo</label>
                <input id="eighth-field" type="file" name="photo" class="form-check" />
            </div>

            <br>

            <div class="entry">
                <input id="btn" type="submit" value="Register">
            </div>
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
    function saveEntry()
    {
        let registrationForm = document.getElementById("RegistrationForm");
        let form_data = new FormData(registrationForm);
            fetch("/api/v1/register", {
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
                .then(function (data) {
                    console.log(data);
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
    .reg_form{
        width: 400px;
    }
    .container-fluid{
        display: flex;
        align-items: center;
        justify-content: center;
    }
    form{
        padding: 2em;
        box-shadow: 3px 3px 3px rgb(192, 202, 206);
        border-radius: 5px;
        border: 2px solid rgb(188, 201, 206);
        background-color: rgb(255, 255, 255);
    }
    #btn{
        width: 100%;
        height: 40px;
        border-radius: 5px;
        border: none;
        background-color: #3de909;
        color: white;
    }
</style>
