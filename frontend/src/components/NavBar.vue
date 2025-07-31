<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top shadow">
    <div class="container-fluid">
      <router-link class="navbar-brand fw-bold" to="/dashboard">
        <i class="fas fa-graduation-cap me-2"></i>
        Quiz Master
      </router-link>
      
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav me-auto">
          <li class="nav-item" v-if="user?.role === 'admin'">
            <router-link class="nav-link" to="/admin">
              <i class="fas fa-tachometer-alt me-1"></i>
              Admin Dashboard
            </router-link>
          </li>
          <li class="nav-item" v-if="user?.role === 'user'">
            <router-link class="nav-link" to="/dashboard">
              <i class="fas fa-user me-1"></i>
              My Dashboard
            </router-link>
          </li>
          <li class="nav-item dropdown" v-if="user?.role === 'admin'">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
              <i class="fas fa-cogs me-1"></i>
              Manage
            </a>
            <ul class="dropdown-menu">
              <li><router-link class="dropdown-item" to="/admin/subjects">
                <i class="fas fa-book me-2"></i>Subjects
              </router-link></li>
              <li><router-link class="dropdown-item" to="/admin/chapters">
                <i class="fas fa-bookmark me-2"></i>Chapters
              </router-link></li>
              <li><router-link class="dropdown-item" to="/admin/quizzes">
                <i class="fas fa-question-circle me-2"></i>Quizzes
              </router-link></li>
            </ul>
          </li>
        </ul>
        
        <ul class="navbar-nav">
          <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">
              <i class="fas fa-user-circle me-1"></i>
              {{ user?.full_name || 'User' }}
            </a>
            <ul class="dropdown-menu dropdown-menu-end">
              <li><h6 class="dropdown-header">{{ user?.email }}</h6></li>
              <li><hr class="dropdown-divider"></li>
              <li><a class="dropdown-item" href="#" @click="logout">
                <i class="fas fa-sign-out-alt me-2"></i>Logout
              </a></li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const user = ref(null)

const loadUser = () => {
  const userData = localStorage.getItem('user')
  if (userData) {
    user.value = JSON.parse(userData)
  }
}

const logout = () => {
  localStorage.removeItem('token')
  localStorage.removeItem('user')
  router.push('/login')
}

onMounted(() => {
  loadUser()
})
</script>

<style scoped>
.navbar {
  z-index: 1030;
}

.navbar-brand {
  font-size: 1.5rem;
}

.nav-link {
  transition: all 0.3s ease;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.1);
  border-radius: 5px;
}

.dropdown-menu {
  border: none;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
}
</style>