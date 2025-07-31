<template>
  <div class="login-container">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6 col-lg-4">
          <div class="card shadow-lg border-0">
            <div class="card-body p-5">
              <div class="text-center mb-4">
                <i class="fas fa-graduation-cap text-primary" style="font-size: 3rem;"></i>
                <h2 class="mt-3 mb-0">Quiz Master</h2>
                <p class="text-muted">Sign in to your account</p>
              </div>
              
              <form @submit.prevent="login">
                <div class="mb-3">
                  <label for="email" class="form-label">Email</label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="fas fa-envelope"></i>
                    </span>
                    <input
                      type="email"
                      class="form-control"
                      id="email"
                      v-model="formData.email"
                      required
                      placeholder="Enter your email"
                    >
                  </div>
                </div>
                
                <div class="mb-4">
                  <label for="password" class="form-label">Password</label>
                  <div class="input-group">
                    <span class="input-group-text">
                      <i class="fas fa-lock"></i>
                    </span>
                    <input
                      type="password"
                      class="form-control"
                      id="password"
                      v-model="formData.password"
                      required
                      placeholder="Enter your password"
                    >
                  </div>
                </div>
                
                <div class="alert alert-danger" v-if="error" role="alert">
                  <i class="fas fa-exclamation-triangle me-2"></i>
                  {{ error }}
                </div>
                
                <button type="submit" class="btn btn-primary w-100 py-2" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  <i v-else class="fas fa-sign-in-alt me-2"></i>
                  {{ loading ? 'Signing in...' : 'Sign In' }}
                </button>
              </form>
              
              <div class="text-center mt-4">
                <p class="mb-0">Don't have an account?</p>
                <router-link to="/register" class="btn btn-outline-primary btn-sm mt-2">
                  <i class="fas fa-user-plus me-1"></i>
                  Create Account
                </router-link>
              </div>
              
              <div class="mt-4 pt-3 border-top">
                <small class="text-muted">
                  <strong>Demo Admin:</strong><br>
                  Email: admin@quizmaster.com<br>
                  Password: admin123
                </small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const loading = ref(false)
const error = ref('')

const formData = ref({
  email: '',
  password: ''
})

const login = async () => {
  loading.value = true
  error.value = ''
  
  try {
    const response = await axios.post('http://localhost:5000/api/auth/login', formData.value)
    
    localStorage.setItem('token', response.data.access_token)
    localStorage.setItem('user', JSON.stringify(response.data.user))
    
    if (response.data.user.role === 'admin') {
      router.push('/admin')
    } else {
      router.push('/dashboard')
    }
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Login failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.card {
  border-radius: 15px;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.input-group-text {
  background: transparent;
  border-right: none;
}

.form-control {
  border-left: none;
}

.form-control:focus {
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
  border-color: #86b7fe;
}

.btn-primary {
  background: linear-gradient(45deg, #007bff, #0056b3);
  border: none;
  border-radius: 10px;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 123, 255, 0.4);
}

.btn-outline-primary {
  border-radius: 20px;
  font-weight: 500;
}
</style>