<script setup>
    import { ref, onMounted } from "vue";
    import { useRoute } from "vue-router";

    const route = useRoute();
    
    let user = ref([]);
    let posts = ref([]);
    let lenPosts = ref([]);
    let csrf_token = ref("");
    let isFollowing = ref(false);

    function Follow(user) {
        isFollowing.value = !isFollowing.value;
        if (isFollowing.value) {
          user.followers++;
        } else {
          user.followers--;
        }
    }

    onMounted(() =>{
    
    fetch("/api/v1/usersp/" + route.params.id)
    .then((response) => response.json())
    .then((data) => {
        //console.log(data)
        user.value = data[0];
        posts.value = user.value.posts;
        lenPosts = posts.value.length;
        
        console.log(user.value);

        // ADD FOLLOW IMPLEMENTATION
           
    })
    .catch((error) => {
        console.log(error);
    });
});

function getProfilePhotoUrl(filename) {
  return "/uploads/" + filename;
}


</script>


<template>
  <div class="container" v-if="user && posts">
  
    <div class="userinfo">
      <div class="photo">
        <img :src="getProfilePhotoUrl(user.profile_photo)" alt="Profile Photo" style="max-width: 150px; max-height: 150px;">
      </div>

      <div class="userdetails">
        <h3>{{ user.firstname }} {{ user.lastname }}</h3>

        <p>{{ user.location }}</p>
        <p>Member Since {{ user.joined_on }}</p>
        <div class="biography">
          <p>{{ user.biography }}</p>
        </div>
      </div>

      <div class="userstats">
        <div class="stat">
          <p class="value"> {{lenPosts}} </p> 
          <p class="label">Posts</p>
        </div>
        <div class="stat">
          <p class="value">{{ user.followers }}</p>
          <p class="label">Followers</p>
        </div>
        <button class="follow" :class="{ following: isFollowing }" @click="Follow(user)">{{ isFollowing ? 'Following' : 'Follow' }}</button>
      </div>
    </div>
    <div class = "posts-list">
    <div class = "instapost-card" v-for = "post in posts">
      <div class = "instapost-image">
        <img :src="getProfilePhotoUrl(post.photo)" alt="User Posts" style="max-width: 150px; max-height: 150px;">
      </div>
    </div>
  </div>
  </div>

</template>

<style>
  .container {
    max-width: 1200px;
    margin: 0 auto;
    font-family: 'Helvetica Neue', sans-serif;
  }

  .userinfo {
    display: flex;

    padding: 20px;
    border: 1px solid #e6e6e6;
    background-color: #fff;
  }

  .photo {
    margin-right: 20px;
    border-radius: 50%;
    overflow: hidden;
    box-shadow: 0 0 0 2px #fff, 0 0 8px rgba(0, 0, 0, 0.1);
  }

  .photo img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

  .userdetails h3 {
    margin: 0;
    font-size: 1.2em;
    padding-right: 20px;
  }

  .userdetails p {
    margin: 5px 0;
    color: #999;
  }

  .biography p {
    margin: 10px 0 0;
    color: #666;
  }

  .userstats {
    display: flex;
    align-items: center;
    margin-top: 20px;
    padding: 0 20px;
    border-top: 1px solid #e6e6e6;
    background-color: #fff;
  }

  .stat {
    padding: 20px;
    text-align: center;
    flex: 1;
  }

  .value {
    margin: 0;
    font-size: 1.2em;
    font-weight: bold;
  }

  .label {
    margin: 5px 0;
    color: #999;
  }

  .follow {
    padding-left: 20px;
    margin-left: auto;
    background-color: #3897f0;
    color: #fff;
    border: none;
    border-radius: 3px;
    padding: 8px 16px;

    cursor: pointer;

  }

  .follow:hover {
    background-color: #2680c2;
  }

  .userposts {
    margin-top: 20px;
    padding: 20px;
    background-color: #fff;
  }

  .userposts p {
    margin: 0;

    font-weight: bold;
    color: #262626;
  }

  .posts-list {
  margin-top: 20px;
  max-width: 1200px;
  display: flex;
  flex-wrap: wrap;
  justify-content: space-between;
  align-items: center;
}

.instapost-card {
  box-sizing: border-box;
  width: calc(30% - 10px);
  margin-bottom: 20px;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
}

.instapost-image {
  position: relative;
  padding-bottom: 100%;
  overflow: hidden;
}

/* .instapost-image img {
  display: block;
  object-fit: cover;

  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
} */

.instapost-image img {
  display: block;
  object-fit: cover;
  width: 100%;
  height: 100%;
  position: absolute;
}
.follow {
  background-color: #3897f0;
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 5px;
  cursor: pointer;
}

.following {
  background-color: #1abc9c;
}

.follow:hover {
  background-color: #1873bb;
}

.following:hover {
  background-color: #16a085;
}


</style>


