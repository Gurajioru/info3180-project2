<script setup>
  import 'bootstrap-icons/font/bootstrap-icons.css';

  const props = defineProps(['posts', 'user']);

  function getProfilePhotoUrl(filename) {
    return "/uploads/" + filename;
  }

  let isLiked = false;

  function toggleLike(posts) {
    isLiked = !isLiked;
    if (isLiked) {
      posts.likes++;
    } else {
      posts.likes--;
    }
  }
</script>

<template>
  <div class="card">
    <div class="user-info">
      <img class="profile-img" :src="getProfilePhotoUrl(posts.profile_photo)" alt="Profile Photo">
      <router-link :to="'/usersp/' + posts.user_id" class="card-link">{{ posts.username }}</router-link>
    </div>

    <div class="instapost-image">
      <img :src="getProfilePhotoUrl(posts.photo)" alt="User Posts" style="max-width: 150px; max-height: 150px;">
    </div>

    <div class="post-info">
      <p class="Caption">{{ posts.caption }}</p>
      <p class="Date">{{ posts.created_on }}</p>
      <div class="like-section">
        <button @click="toggleLike(posts)" :class="{ 'liked': isLiked }">
          <i :class="[isLiked ? 'bi bi-heart-fill' : 'bi bi-heart']"></i> {{ posts.likes }} Likes
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>


.card {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
}


.user-info {
  display: flex;
  align-items: center;
  margin: 10px;
}


.user-info img {
 width: 50px;
  max-height: auto;
  border-radius: 100%;
  margin-right: 10px;
}

.instapost-image {
  margin-top: 10px;
}

.instapost-image img {
  max-width: 500px;
  max-height: 500px;
  width: 100%;
  height: auto;
}

.post-info {
  margin: 10px;
}

.Caption {
  font-weight: bold;
  margin-bottom: 5px;
}

.Date {
  font-size: 14px;
  color: grey;
  margin-bottom: 5px;
}
.like-section {
    display: flex;
    align-items: center;
    margin-top: 10px;
  }

  .like-section button {
    display: flex;
    align-items: center;
    font-size: 16px;
    color: #333;
    background-color: transparent;
    border: none;
    cursor: pointer;
  }

  .like-section button:focus {
    outline: none;
  }

  .like-section button i {
    font-size: 20px;
    margin-right: 5px;
  }

  .like-section button.liked {
    color: red;
  }
</style>





