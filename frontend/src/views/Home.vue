<template>
  <div>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card class="pa-6">
          <v-card-title class="text-h4 text-center mb-4">
            Welcome to Full Stack App
          </v-card-title>
          
          <v-card-text class="text-body-1">
            <p class="mb-4">
              This is a full-stack application built with Django and Vue.js, featuring:
            </p>
            
            <v-list>
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="success">mdi-check-circle</v-icon>
                </template>
                <v-list-item-title>Django Backend with REST API</v-list-item-title>
              </v-list-item>
              
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="success">mdi-check-circle</v-icon>
                </template>
                <v-list-item-title>Vue 3 Frontend with Vuetify</v-list-item-title>
              </v-list-item>
              
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="success">mdi-check-circle</v-icon>
                </template>
                <v-list-item-title>OIDC Authentication with U-M Shibboleth</v-list-item-title>
              </v-list-item>
              
              <v-list-item>
                <template v-slot:prepend>
                  <v-icon color="success">mdi-check-circle</v-icon>
                </template>
                <v-list-item-title>Protected and Public API Endpoints</v-list-item-title>
              </v-list-item>
            </v-list>
            
            <v-divider class="my-6"></v-divider>
            
            <v-alert
              v-if="!isAuthenticated"
              type="info"
              variant="tonal"
              class="mb-4"
            >
              <strong>Get Started:</strong> Click the Login button to access protected features using your U-M credentials.
            </v-alert>
            
            <v-alert
              v-else
              type="success"
              variant="tonal"
              class="mb-4"
            >
              <strong>Welcome back, {{ user?.username || user?.first_name || 'User' }}!</strong> You can now access all protected features.
            </v-alert>
          </v-card-text>
          
          <v-card-actions class="justify-center">
            <v-btn
              v-if="!isAuthenticated"
              @click="login"
              color="primary"
              size="large"
            >
              Login with U-M
            </v-btn>
            
            <v-btn
              v-else
              to="/models"
              color="primary"
              size="large"
            >
              View Models
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

export default {
  name: 'Home',
  setup() {
    const authStore = useAuthStore()
    
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    const user = computed(() => authStore.user)
    
    const login = () => {
      // Use the auth store login method which handles mode detection
      authStore.login()
    }
    
    return {
      isAuthenticated,
      user,
      login
    }
  }
}
</script>
