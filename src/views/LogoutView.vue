<script setup>
    import { ref } from "vue";
    let message = ref("Hello World! This is a VueJS and Flask Starter Template.")
</script>

<template>
    <div class="container">
      <div class="contain">
        <div class="center">
          <img :src="`/uploads/uyuni.jpg`" alt="Photogram" class="uyuni" />
          <div class="secondary">
            <div class="together">
              <img :src="`/uploads/camera.jpg`" alt="Photogram" class="camera" />
              <h2 class="title">Photogram</h2>
            </div>
  
            <div class="text">
              <h4>You have successfully logged out.</h4>
            </div>
  
            <br>
            <br>
            <br>
  
            <div class="buttons">
              <a href="/register" class="btn1">Register</a>
              <a href="/login" class="btn2">Login</a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>

<style>
  .btn1{
    background-color: #3ec93e;
    border: none;
    border-radius: 5px;
    color: white;
    height: 50px;
    width: 200px;
    align-items: center;
    display: flex;
    justify-content: center;
    text-decoration: none;
  }
  .btn2{
    background-color: #6379f7;
    border: none;
    border-radius: 5px;
    color: white;
    height: 50px;
    width: 200px;
    align-items: center;
    display: flex;
    justify-content: center;
    text-decoration: none;
  }
  .buttons{
    display: grid;
    grid-template-columns: 210px 210px;
    justify-content: center;
  }
  .camera{
    margin-right: 30px;
    width: 30px;
    height: 30px;
  }
  
  .together{
    display: flex;
    justify-content: center;
  }
  .center{
    display: grid;
    grid-template-columns: 600px 600px;
    width: 810px;
    position: absolute;
    top: 22.5%;
    left: 10.25%;
  }
  .uyuni{
    width: 500px;
    height: 400px;
    border-radius: 5px;
    box-shadow: 3px 3px 3px rgb(191, 197, 199);
  }
  
  .secondary{
    width: 600px;
    height: 400px;
    border-radius: 5px;
    box-shadow: 3px 3px 3px rgb(191, 197, 199);
    border: 2px solid rgb(191, 197, 199);
    padding: 30px;
    background-color: rgb(244, 242, 242);
  }
  .contain{
    width: 1300px;
    height: 600px;
  }
  
  .title{
    font-family: Lucida Handwriting;
    font-weight: 900;
  }
</style>
