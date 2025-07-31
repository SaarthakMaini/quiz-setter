import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import App from './App.vue'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.bundle.min.js'
import LoginPage from './components/LoginPage.vue'
import RegisterPage from './components/RegisterPage.vue'
import AdminDashboard from './components/AdminDashboard.vue'
import UserDashboard from './components/UserDashboard.vue'
import QuizInterface from './components/QuizInterface.vue'
import SubjectManagement from './components/SubjectManagement.vue'
import ChapterManagement from './components/ChapterManagement.vue'
import QuizManagement from './components/QuizManagement.vue'
import QuestionManagement from './components/QuestionManagement.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginPage },
  { path: '/register', component: RegisterPage },
  { path: '/admin', component: AdminDashboard, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/dashboard', component: UserDashboard, meta: { requiresAuth: true } },
  { path: '/quiz/:id', component: QuizInterface, meta: { requiresAuth: true } },
  { path: '/admin/subjects', component: SubjectManagement, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/admin/chapters', component: ChapterManagement, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/admin/quizzes', component: QuizManagement, meta: { requiresAuth: true, requiresAdmin: true } },
  { path: '/admin/questions/:quizId', component: QuestionManagement, meta: { requiresAuth: true, requiresAdmin: true } }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  const user = localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user') || '{}') : null
  
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.meta.requiresAdmin && user?.role !== 'admin') {
    next('/dashboard')
  } else {
    next()
  }
})

const app = createApp(App)
app.use(router)
app.mount('#app')