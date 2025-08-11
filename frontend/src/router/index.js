import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Models from '@/views/Models.vue'
import Model1 from '@/views/Model1.vue'
import Model2 from '@/views/Model2.vue'
import Contact from '@/views/Contact.vue'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/models',
    name: 'Models',
    component: Models
  },
  {
    path: '/models/model1',
    name: 'Model1',
    component: Model1,
    meta: { requiresAuth: false }
  },
  {
    path: '/models/model2',
    name: 'Model2',
    component: Model2,
    meta: { requiresAuth: true }
  },
  {
    path: '/contact',
    name: 'Contact',
    component: Contact
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guard for authenticated routes
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    // Use the auth store login method which handles mode detection
    authStore.login()
    return
  } else {
    next()
  }
})

export default router
