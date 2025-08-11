<template>
  <v-app>
    <!-- Header with Navigation -->
    <v-app-bar app color="primary" dark>
      <v-app-bar-title>Full Stack App</v-app-bar-title>
      
      <v-spacer></v-spacer>
      
      <v-btn
        v-for="item in navigationItems"
        :key="item.title"
        :to="item.path"
        text
        class="mx-2"
      >
        {{ item.title }}
      </v-btn>
      
      <v-btn
        v-if="!isAuthenticated"
        @click="login"
        color="secondary"
        class="ml-4"
      >
        Login with U-M
      </v-btn>
      
      <v-btn
        v-else
        @click="logout"
        color="secondary"
        class="ml-4"
      >
        {{ user?.username || 'User' }} (Logout)
      </v-btn>
    </v-app-bar>

    <!-- Main Content -->
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>

    <!-- Footer -->
    <v-footer app color="grey darken-3" dark>
      <v-row justify="center" no-gutters>
        <v-col class="text-center" cols="12">
          <span>&copy; {{ new Date().getFullYear() }} Full Stack App. Built with Django + Vue + Vuetify.</span>
        </v-col>
      </v-row>
    </v-footer>
  </v-app>
</template>

<script>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'App',
  setup() {
    const router = useRouter()
    const authStore = useAuthStore()
    
    const navigationItems = ref([
      { title: 'Home', path: '/' },
      { 
        title: 'Models', 
        path: '/models',
        children: [
          { title: 'Model 1', path: '/models/model1' },
          { title: 'Model 2', path: '/models/model2' }
        ]
      },
      { title: 'Contact', path: '/contact' }
    ])

    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const user = computed(() => authStore.user)

    const login = () => {
      // Use the auth store login method which handles mode detection
      authStore.login()
    }

    const logout = () => {
      authStore.logout()
      router.push('/')
    }

    return {
      navigationItems,
      isAuthenticated,
      user,
      login,
      logout
    }
  }
}
</script>

<style>
.v-main {
  min-height: calc(100vh - 128px);
}
</style>
