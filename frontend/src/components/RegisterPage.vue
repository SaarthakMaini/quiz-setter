<template>
  <div class="register-container">
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
          <div class="card shadow-lg border-0">
            <div class="card-body p-5">
              <div class="text-center mb-4">
                <i class="fas fa-user-plus text-primary" style="font-size: 3rem;"></i>
                <h2 class="mt-3 mb-0">Create Account</h2>
                <p class="text-muted">Join Quiz Master today</p>
              </div>
              
              <form @submit.prevent="register">
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="username" class="form-label">Username</label>
                    <input
                      type="text"
                      class="form-control"
                      id="username"
                      v-model="formData.username"
                      required
                      placeholder="Choose a username"
                    >
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label for="email" class="form-label">Email</label>
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
                
                <div class="mb-3">
                  <label for="full_name" class="form-label">Full Name</label>
                  <input
                    type="text"
                    class="form-control"
                    id="full_name"
                    v-model="formData.full_name"
                    required
                    placeholder="Enter your full name"
                  >
                </div>
                
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label for="qualification" class="form-label">Qualification</label>
                    <select class="form-select" id="qualification" v-model="formData.qualification">
                      <option value="">Select qualification</option>
                      <option value="High School">High School</option>
                      <option value="Bachelor's Degree">Bachelor's Degree</option>
                      <option value="Master's Degree">Master's Degree</option>
                      <option value="PhD">PhD</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                  
                  <div class="col-md-6 mb-3">
                    <label for="date_of_birth" class="form-label">Date of Birth</label>
                    <input
                      type="date"
                      class="form-control"
                      id="date_of_birth"
                      v-model="formData.date_of_birth"
                    >
                  </div>
                </div>
                
                <div class="mb-4">
                  <label for="password" class="form-label">Password</label>
                  <input
                    type="password"
                    class="form-control"
                    id="password"
                    v-model="formData.password"
                    required
                    placeholder="Create a password"
                    minlength="6"
                  >
                  <div class="form-text">Password must be at least 6 characters long</div>
                </div>
                
                <div class="alert alert-danger" v-if="error" role="alert">
                  <i class="fas fa-exclamation-triangle me-2"></i>
                  {{ error }}
                </div>
                
                <div class="alert alert-success" v-if="success" role="alert">
                  <i class="fas fa-check-circle me-2"></i>
                  {{ success }}
                </div>
                
                <button type="submit" class="btn btn-primary w-100 py-2" :disabled="loading">
                  <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                  <i v-else class="fas fa-user-plus me-2"></i>
                  {{ loading ? 'Creating Account...' : 'Create Account' }}
                </button>
              </form>
              
              <div class="text-center mt-4">
                <p class="mb-0">Already have an account?</p>
                <router-link to="/login" class="btn btn-outline-primary btn-sm mt-2">
                  <i class="fas fa-sign-in-alt me-1"></i>
                  Sign In
                </router-link>
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
const success = ref('')

const formData = ref({
  username: '',
  email: '',
  password: '',
  full_name: '',
  qualification: '',
  date_of_birth: ''
})

const register = async () => {
  loading.value = true
  error.value = ''
  success.value = ''
  
  try {
    await axios.post('http://localhost:5000/api/auth/register', formData.value)
    
    success.value = 'Account created successfully! Redirecting to login...'
    
    setTimeout(() => {
      router.push('/login')
    }, 2000)
  } catch (err: any) {
    error.value = err.response?.data?.error || 'Registration failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px 0;
}

.card {
  border-radius: 15px;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95);
}

.form-control, .form-select {
  border-radius: 8px;
  border: 1px solid #ddd;
  transition: all 0.3s ease;
}

.form-control:focus, .form-select:focus {
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
  border-color: #86b7fe;
  transform: translateY(-1px);
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