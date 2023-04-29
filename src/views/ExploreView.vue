<script setup>
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";
import { RouterLink } from "vue-router";
import PostCard from "../components/PostCard.vue";

let posts = ref([]);
let user = ref([]);
let likes = ref([]);
const route = useRoute();
let loading = ref(false);

onMounted(() => {
    
    loading.value = true;

    fetch("/api/v1/users")
    .then((response) => response.json())
    .then((data) => {
      user.value = data.response;
      //for (let i = 0; i < user.value.length; i++){
        //console.log(user.value[i].username);
      //}
      //console.log(getUser(1));
    })
    .catch((error) => {
      console.log(error);
    });

    fetch("/api/v1/likes")
    .then((response) => response.json())
    .then((data) => {
      likes.value = data.response;
      //console.log(likes.value);
    })
    .catch((error) => {
      console.log(error);
    });

    fetch("/api/v1/posts")
        .then((response) => response.json())
        .then((data) => {
        
        posts.value = data;
        loading.value = false;
         for (let i = 0; i < posts.value.length; i++) {
            const post = posts.value[i];
            console.log((getUser(post.user_id)).username);
            post.username = (getUser(post.user_id)).username;
            post.likes = getLikes(post.id);
            post.profile_photo = (getUser(post.user_id)).profile_photo;
         }
         console.log(posts.value);
         
        })
        .catch((error) => {
        console.log(error);
        });


    
});

function getPostLikes(postId) {
  return fetch(`/api/v1/postlikes/${postId}`)
    .then((response) => response.json())
    .then((data) => {
      return data;
    })
    .catch((error) => {
      console.log(error);
      return null;
    });
}


function getLikes(postID){
    let count = 0;
    if (likes.value && likes.value.length > 0) {
        for (let l of likes.value){
            if (l.post_id === postID){
                count++;
            }
        }
    }
    return count;
}

function getUser(userId) {
  if (user.value && user.value.length > 0) {
    for (let u of user.value) {
      if (u.id === userId) {
        return { username: u.username, profile_photo: u.profile_photo };
      }
    }
  }
  return { username: "", profile_photo: "" };
}

</script>

<template>
    <div class="container">
        <div class = "Post-Container">
            <PostCard :posts="post"  v-for="post in posts" :key="post.id" />
        </div>
        
    </div>


</template>