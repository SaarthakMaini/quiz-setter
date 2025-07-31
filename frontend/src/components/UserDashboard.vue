<template>
  <div class="dashboard-container">
    <div class="container-fluid py-4">
      <div class="row mb-4">
        <div class="col-12">
          <div class="card bg-primary text-white">
            <div class="card-body">
              <div class="row align-items-center">
                <div class="col-md-8">
                  <h2 class="mb-1">Welcome back, {{ user?.full_name }}!</h2>
                  <p class="mb-0 opacity-75">Ready to test your knowledge? Choose a quiz below or check your progress.</p>
                </div>
                <div class="col-md-4 text-end">
                  <i class="fas fa-user-graduate" style="font-size: 4rem; opacity: 0.3;"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row mb-4">
        <div class="col-md-3 mb-3">
          <div class="card border-0 shadow-sm">
            <div class="card-body text-center">
              <div class="text-primary mb-2">
                <i class="fas fa-clipboard-list fa-2x"></i>
              </div>
              <h4 class="fw-bold">{{ stats.total_attempts || 0 }}</h4>
              <p class="text-muted mb-0">Quiz Attempts</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-3 mb-3">
          <div class="card border-0 shadow-sm">
            <div class="card-body text-center">
              <div class="text-success mb-2">
                <i class="fas fa-chart-line fa-2x"></i>
              </div>
              <h4 class="fw-bold">{{ Math.round(stats.average_score || 0) }}%</h4>
              <p class="text-muted mb-0">Average Score</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-3 mb-3">
          <div class="card border-0 shadow-sm">
            <div class="card-body text-center">
              <div class="text-warning mb-2">
                <i class="fas fa-trophy fa-2x"></i>
              </div>
              <h4 class="fw-bold">{{ Math.round(stats.best_score || 0) }}%</h4>
              <p class="text-muted mb-0">Best Score</p>
            </div>
          </div>
        </div>
        
        <div class="col-md-3 mb-3">
          <div class="card border-0 shadow-sm">
            <div class="card-body text-center">
              <div class="text-info mb-2">
                <i class="fas fa-medal fa-2x"></i>
              </div>
              <h4 class="fw-bold">{{ getRank() }}</h4>
              <p class="text-muted mb-0">Performance</p>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-lg-8 mb-4">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-0 pb-0">
              <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">
                  <i class="fas fa-question-circle text-primary me-2"></i>
                  Available Quizzes
                </h5>
                <div class="input-group" style="width: 300px;">
                  <span class="input-group-text">
                    <i class="fas fa-search"></i>
                  </span>
                  <input
                    type="text"
                    class="form-control"
                    placeholder="Search quizzes..."
                    v-model="searchQuery"
                  >
                </div>
              </div>
            </div>
            <div class="card-body">
              <div class="row" v-if="filteredQuizzes.length > 0">
                <div class="col-md-6 mb-3" v-for="quiz in filteredQuizzes" :key="quiz.id">
                  <div class="card h-100 border-0 shadow-sm quiz-card">
                    <div class="card-body">
                      <div class="d-flex justify-content-between align-items-start mb-2">
                        <h6 class="card-title mb-0">{{ quiz.title }}</h6>
                        <span class="badge bg-primary">{{ quiz.questions_count }} Q</span>
                      </div>
                      <p class="text-muted small mb-2">
                        <i class="fas fa-book me-1"></i>{{ quiz.subject_name }} - {{ quiz.chapter_name }}
                      </p>
                      <p class="text-muted small mb-3">
                        <i class="fas fa-clock me-1"></i>{{ quiz.time_duration }} minutes
                        <span class="ms-3">
                          <i class="fas fa-users me-1"></i>{{ quiz.attempts_count }} attempts
                        </span>
                      </p>
                      <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                          {{ formatDate(quiz.date_of_quiz) }}
                        </small>
                        <button
                          class="btn btn-primary btn-sm"
                          @click="startQuiz(quiz.id)"
                          :disabled="!quiz.is_active"
                        >
                          <i class="fas fa-play me-1"></i>
                          {{ quiz.is_active ? 'Start Quiz' : 'Inactive' }}
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-4">
                <i class="fas fa-question-circle text-muted" style="font-size: 3rem;"></i>
                <p class="text-muted mt-3">No quizzes found matching your search.</p>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-4">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-0 pb-0">
              <h5 class="mb-0">
                <i class="fas fa-history text-success me-2"></i>
                Recent Attempts
              </h5>
            </div>
            <div class="card-body">
              <div v-if="stats.recent_attempts && stats.recent_attempts.length > 0">
                <div
                  class="d-flex align-items-center mb-3 p-2 rounded attempt-item"
                  v-for="attempt in stats.recent_attempts.slice(0, 5)"
                  :key="attempt.id"
                >
                  <div class="flex-shrink-0 me-3">
                    <div class="score-circle" :class="getScoreClass(attempt.percentage)">
                      {{ Math.round(attempt.percentage) }}%
                    </div>
                  </div>
                  <div class="flex-grow-1">
                    <h6 class="mb-1 small">{{ attempt.quiz_title }}</h6>
                    <p class="text-muted small mb-0">
                      {{ attempt.chapter_name }}
                    </p>
                    <small class="text-muted">
                      {{ formatDate(attempt.timestamp_of_attempt) }}
                    </small>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-4">
                <i class="fas fa-clipboard-list text-muted" style="font-size: 2rem;"></i>
                <p class="text-muted mt-2">No quiz attempts yet.</p>
                <small class="text-muted">Start a quiz to see your results here!</small>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const user = ref(null)
const quizzes = ref([])
const stats = ref({})
const searchQuery = ref('')

const filteredQuizzes = computed(() => {
  if (!searchQuery.value) return quizzes.value
  
  return quizzes.value.filter(quiz =>
    quiz.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    quiz.subject_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    quiz.chapter_name.toLowerCase().includes(searchQuery.value.toLowerCase())
  )
})

const loadUser = () => {
  const userData = localStorage.getItem('user')
  if (userData) {
    user.value = JSON.parse(userData)
  }
}

const loadQuizzes = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://localhost:5000/api/quizzes', {
      headers: { Authorization: `Bearer ${token}` }
    })
    quizzes.value = response.data
  } catch (error) {
    console.error('Error loading quizzes:', error)
  }
}

const loadStats = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://localhost:5000/api/dashboard/stats', {
      headers: { Authorization: `Bearer ${token}` }
    })
    stats.value = response.data
  } catch (error) {
    console.error('Error loading stats:', error)
  }
}

const startQuiz = (quizId: number) => {
  router.push(`/quiz/${quizId}`)
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

const getRank = () => {
  const avg = stats.value.average_score || 0
  if (avg >= 90) return 'Excellent'
  if (avg >= 80) return 'Very Good'
  if (avg >= 70) return 'Good'
  if (avg >= 60) return 'Average'
  return 'Needs Work'
}

const getScoreClass = (percentage: number) => {
  if (percentage >= 90) return 'excellent'
  if (percentage >= 80) return 'very-good'
  if (percentage >= 70) return 'good'
  if (percentage >= 60) return 'average'
  return 'needs-work'
}

onMounted(() => {
  loadUser()
  loadQuizzes()
  loadStats()
})
</script>

<style scoped>
.dashboard-container {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.quiz-card {
  transition: all 0.3s ease;
  cursor: pointer;
}

.quiz-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
}

.attempt-item {
  background-color: #f8f9fa;
  transition: all 0.3s ease;
}

.attempt-item:hover {
  background-color: #e9ecef;
}

.score-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.8rem;
  color: white;
  text-align: center;
}

.score-circle.excellent {
  background: linear-gradient(135deg, #28a745, #20c997);
}

.score-circle.very-good {
  background: linear-gradient(135deg, #17a2b8, #007bff);
}

.score-circle.good {
  background: linear-gradient(135deg, #ffc107, #fd7e14);
}

.score-circle.average {
  background: linear-gradient(135deg, #fd7e14, #dc3545);
}

.score-circle.needs-work {
  background: linear-gradient(135deg, #dc3545, #6f42c1);
}

.card {
  border-radius: 12px;
}

.btn-primary {
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
}

.input-group-text {
  background: transparent;
  border: 1px solid #ddd;
}

.form-control {
  border: 1px solid #ddd;
}

.form-control:focus {
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.15);
  border-color: #86b7fe;
}
</style>