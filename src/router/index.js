import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      component: () => import('../views/AddPostForm.vue')
    },
    {
      path: '/usersp/:id',
      name: 'Users',
      component: () => import('../views/UsersView.vue')
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/UserRegistrationView.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/LoginView.vue')
    },
    {
    path: '/explore',
    name: 'ExploreView',
    component: () => import('../views/ExploreView.vue')
    }
  ]
})

export default router
