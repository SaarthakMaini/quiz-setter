<template>
  <div id="app">
    <NavBar v-if="isAuthenticated" />
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from './components/NavBar.vue'

const router = useRouter()
const isAuthenticated = ref(false)

const checkAuth = () => {
  const token = localStorage.getItem('token')
  isAuthenticated.value = !!token
}

onMounted(() => {
  checkAuth()
  
  // Listen for storage changes (login/logout from other tabs)
  window.addEventListener('storage', checkAuth)
})

// Watch for route changes to update auth status
router.afterEach(() => {
  checkAuth()
})
</script>

<style scoped>
#app {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.main-content {
  min-height: calc(100vh - 60px);
  padding-top: 60px;
}

.main-content.no-nav {
  padding-top: 0;
}
</style>