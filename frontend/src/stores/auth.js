import { defineStore } from 'pinia'
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const isAuthenticated = ref(false)
  const loading = ref(true)

  // Check authentication status on mount
  onMounted(() => {
    checkAuthStatus()
  })

  const checkAuthStatus = async () => {
    try {
      console.log('🔍 Checking authentication status...')
      // Try to get current user info from Django
      const response = await axios.get('/api/auth/user/', { withCredentials: true })
      user.value = response.data
      isAuthenticated.value = true
      
      // Log user info for debugging (remove in production)
      console.log('✅ User authenticated:', response.data)
    } catch (error) {
      // User is not authenticated
      user.value = null
      isAuthenticated.value = false
      console.log('❌ User not authenticated:', error.message)
    } finally {
      loading.value = false
    }
  }

  const login = () => {
    console.log('🚀 Login button clicked, checking backend mode...')
    // Check backend mode by trying to access a mode endpoint
    checkBackendMode().then(mode => {
      console.log('🎯 Backend mode determined:', mode)
      if (mode === 'LOCAL') {
        // Local mode: use mock login
        console.log('🔧 Local mode: Using mock login')
        mockLogin()
      } else {
        // Production mode: redirect to U-M OIDC
        console.log('🚀 Production mode: Redirecting to U-M OIDC')
        window.location.href = '/oidc/authenticate/'
      }
    }).catch((error) => {
      // Fallback to mock login if can't determine mode
      console.log('🔧 Fallback: Using mock login due to error:', error)
      mockLogin()
    })
  }

  const logout = () => {
    checkBackendMode().then(mode => {
      if (mode === 'LOCAL') {
        // Local mode: use mock logout
        console.log('🔧 Local mode: Using mock logout')
        mockLogout()
        // Clear local user state
        user.value = null
        isAuthenticated.value = false
      } else {
        // Production mode: redirect to U-M OIDC logout
        console.log('🚀 Production mode: Redirecting to U-M OIDC logout')
        window.location.href = '/oidc/logout/'
      }
    }).catch(() => {
      // Fallback to mock logout if can't determine mode
      console.log('🔧 Fallback: Using mock logout')
      mockLogout()
      // Clear local user state
      user.value = null
      isAuthenticated.value = false
    })
  }

  const checkBackendMode = async () => {
    try {
      console.log('🔍 Checking backend mode...')
      const response = await axios.get('/api/public/public_info/')
      const mode = response.data.mode || 'LOCAL'
      console.log('🔍 Backend mode detected:', mode)
      return mode
    } catch (error) {
      console.log('Could not determine backend mode, defaulting to LOCAL')
      return 'LOCAL'
    }
  }

  const mockLogin = async () => {
    try {
      console.log('🔧 Starting mock login...')
      loading.value = true
      const response = await axios.post('/api/auth/mock_login/', {}, { withCredentials: true })
      
      console.log('✅ Mock login successful:', response.data)
      
      // Refresh auth status
      console.log('🔄 Refreshing auth status...')
      await checkAuthStatus()
      
    } catch (error) {
      console.error('❌ Mock login failed:', error)
    } finally {
      loading.value = false
    }
  }

  const mockLogout = async () => {
    try {
      await axios.post('/api/auth/mock_logout/', {}, { withCredentials: true })
      console.log('Mock logout successful')
      
      // Clear local state
      user.value = null
      isAuthenticated.value = false
      
    } catch (error) {
      console.error('Mock logout failed:', error)
    }
  }

  const handleAuthCallback = async () => {
    // This will be called after OIDC redirect back to the app
    await checkAuthStatus()
  }

  return {
    user,
    isAuthenticated,
    loading,
    login,
    logout,
    checkAuthStatus,
    handleAuthCallback,
    mockLogin,
    mockLogout
  }
})
