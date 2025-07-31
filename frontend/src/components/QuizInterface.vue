<template>
  <div class="quiz-container">
    <div class="container-fluid py-4" v-if="!loading">
      <div class="row mb-4">
        <div class="col-12">
          <div class="card border-0 shadow-sm">
            <div class="card-body">
              <div class="row align-items-center">
                <div class="col-md-8">
                  <h3 class="mb-2">{{ quiz.title }}</h3>
                  <p class="text-muted mb-0">
                    <i class="fas fa-book me-2"></i>{{ quiz.subject_name }} - {{ quiz.chapter_name }}
                  </p>
                </div>
                <div class="col-md-4 text-end">
                  <div class="timer-display" :class="{ 'timer-warning': timeRemaining < 300 }">
                    <i class="fas fa-clock me-2"></i>
                    <span class="fw-bold">{{ formatTime(timeRemaining) }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row mb-4">
        <div class="col-12">
          <div class="progress" style="height: 8px;">
            <div
              class="progress-bar bg-primary"
              :style="{ width: progressPercentage + '%' }"
              role="progressbar"
            ></div>
          </div>
          <div class="d-flex justify-content-between mt-2">
            <small class="text-muted">Question {{ currentQuestionIndex + 1 }} of {{ questions.length }}</small>
            <small class="text-muted">{{ Math.round(progressPercentage) }}% Complete</small>
          </div>
        </div>
      </div>

      <div class="row justify-content-center" v-if="!showResults">
        <div class="col-lg-8">
          <div class="card border-0 shadow-sm question-card">
            <div class="card-body p-4">
              <div class="question-number mb-3">
                <span class="badge bg-primary fs-6">Question {{ currentQuestionIndex + 1 }}</span>
              </div>
              
              <h4 class="question-text mb-4">{{ currentQuestion.question_statement }}</h4>
              
              <div class="options-container">
                <div
                  class="option-item mb-3"
                  v-for="(option, index) in getOptions(currentQuestion)"
                  :key="index"
                  @click="selectOption(index + 1)"
                >
                  <div class="form-check">
                    <input
                      class="form-check-input"
                      type="radio"
                      :id="`option${index + 1}`"
                      :value="index + 1"
                      v-model="selectedAnswers[currentQuestion.id]"
                    >
                    <label class="form-check-label w-100" :for="`option${index + 1}`">
                      <div class="option-content">
                        <div class="option-letter">{{ String.fromCharCode(65 + index) }}</div>
                        <div class="option-text">{{ option }}</div>
                      </div>
                    </label>
                  </div>
                </div>
              </div>
              
              <div class="navigation-buttons mt-4 d-flex justify-content-between">
                <button
                  class="btn btn-outline-secondary"
                  @click="previousQuestion"
                  :disabled="currentQuestionIndex === 0"
                >
                  <i class="fas fa-chevron-left me-2"></i>Previous
                </button>
                
                <button
                  class="btn btn-primary"
                  @click="nextQuestion"
                  v-if="currentQuestionIndex < questions.length - 1"
                >
                  Next<i class="fas fa-chevron-right ms-2"></i>
                </button>
                
                <button
                  class="btn btn-success"
                  @click="submitQuiz"
                  v-else
                  :disabled="!canSubmit"
                >
                  <i class="fas fa-check me-2"></i>Submit Quiz
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row justify-content-center" v-if="showResults">
        <div class="col-lg-8">
          <div class="card border-0 shadow-sm">
            <div class="card-body text-center p-5">
              <div class="result-icon mb-4">
                <i class="fas fa-trophy text-warning" style="font-size: 4rem;" v-if="results.percentage >= 80"></i>
                <i class="fas fa-medal text-success" style="font-size: 4rem;" v-else-if="results.percentage >= 60"></i>
                <i class="fas fa-clipboard-check text-info" style="font-size: 4rem;" v-else></i>
              </div>
              
              <h2 class="mb-3">Quiz Completed!</h2>
              <p class="text-muted mb-4">Here are your results:</p>
              
              <div class="row mb-4">
                <div class="col-md-3 mb-3">
                  <div class="stat-card">
                    <h3 class="text-primary">{{ results.total_scored }}</h3>
                    <p class="text-muted">Correct Answers</p>
                  </div>
                </div>
                <div class="col-md-3 mb-3">
                  <div class="stat-card">
                    <h3 class="text-secondary">{{ results.total_possible }}</h3>
                    <p class="text-muted">Total Questions</p>
                  </div>
                </div>
                <div class="col-md-3 mb-3">
                  <div class="stat-card">
                    <h3 class="text-success">{{ Math.round(results.percentage) }}%</h3>
                    <p class="text-muted">Score</p>
                  </div>
                </div>
                <div class="col-md-3 mb-3">
                  <div class="stat-card">
                    <h3 class="text-info">{{ formatTime(timeTaken) }}</h3>
                    <p class="text-muted">Time Taken</p>
                  </div>
                </div>
              </div>
              
              <div class="performance-message mb-4 p-3 rounded" :class="getPerformanceClass(results.percentage)">
                <h5 class="mb-2">{{ getPerformanceMessage(results.percentage) }}</h5>
                <p class="mb-0">{{ getPerformanceDescription(results.percentage) }}</p>
              </div>
              
              <div class="action-buttons">
                <button class="btn btn-primary me-3" @click="goToDashboard">
                  <i class="fas fa-home me-2"></i>Back to Dashboard
                </button>
                <button class="btn btn-outline-secondary" @click="retakeQuiz">
                  <i class="fas fa-redo me-2"></i>Retake Quiz
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="d-flex justify-content-center align-items-center" style="height: 50vh;" v-if="loading">
      <div class="text-center">
        <div class="spinner-border text-primary mb-3" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="text-muted">Loading quiz...</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const loading = ref(true)
const quiz = ref({})
const questions = ref([])
const currentQuestionIndex = ref(0)
const selectedAnswers = ref({})
const timeRemaining = ref(0)
const timer = ref(null)
const showResults = ref(false)
const results = ref({})
const startTime = ref(0)
const timeTaken = ref(0)

const currentQuestion = computed(() => questions.value[currentQuestionIndex.value] || {})
const progressPercentage = computed(() => ((currentQuestionIndex.value + 1) / questions.value.length) * 100)
const canSubmit = computed(() => {
  return Object.keys(selectedAnswers.value).length >= questions.value.length
})

const loadQuiz = async () => {
  try {
    const token = localStorage.getItem('token')
    const quizId = route.params.id
    
    const quizResponse = await axios.get(`http://localhost:5000/api/quizzes`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    const quizData = quizResponse.data.find(q => q.id === parseInt(quizId))
    if (!quizData) {
      throw new Error('Quiz not found')
    }
    
    quiz.value = quizData
    
    const questionsResponse = await axios.get(`http://localhost:5000/api/quizzes/${quizId}/questions`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    questions.value = questionsResponse.data
    timeRemaining.value = quiz.value.time_duration * 60 // Convert to seconds
    startTime.value = Date.now()
    
    startTimer()
    loading.value = false
  } catch (error) {
    console.error('Error loading quiz:', error)
    router.push('/dashboard')
  }
}

const startTimer = () => {
  timer.value = setInterval(() => {
    timeRemaining.value--
    if (timeRemaining.value <= 0) {
      submitQuiz()
    }
  }, 1000)
}

const formatTime = (seconds) => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes.toString().padStart(2, '0')}:${remainingSeconds.toString().padStart(2, '0')}`
}

const getOptions = (question) => {
  const options = [question.option1, question.option2]
  if (question.option3) options.push(question.option3)
  if (question.option4) options.push(question.option4)
  return options
}

const selectOption = (optionIndex) => {
  selectedAnswers.value[currentQuestion.value.id] = optionIndex
}

const nextQuestion = () => {
  if (currentQuestionIndex.value < questions.value.length - 1) {
    currentQuestionIndex.value++
  }
}

const previousQuestion = () => {
  if (currentQuestionIndex.value > 0) {
    currentQuestionIndex.value--
  }
}

const submitQuiz = async () => {
  try {
    if (timer.value) {
      clearInterval(timer.value)
    }
    
    timeTaken.value = Math.floor((Date.now() - startTime.value) / 1000)
    
    const token = localStorage.getItem('token')
    const response = await axios.post(
      `http://localhost:5000/api/quizzes/${route.params.id}/submit`,
      {
        answers: selectedAnswers.value,
        time_taken: timeTaken.value
      },
      {
        headers: { Authorization: `Bearer ${token}` }
      }
    )
    
    results.value = response.data.score
    showResults.value = true
  } catch (error) {
    console.error('Error submitting quiz:', error)
  }
}

const getPerformanceClass = (percentage) => {
  if (percentage >= 90) return 'bg-success text-white'
  if (percentage >= 80) return 'bg-primary text-white'
  if (percentage >= 70) return 'bg-warning text-dark'
  if (percentage >= 60) return 'bg-info text-white'
  return 'bg-danger text-white'
}

const getPerformanceMessage = (percentage) => {
  if (percentage >= 90) return 'Outstanding Performance!'
  if (percentage >= 80) return 'Excellent Work!'
  if (percentage >= 70) return 'Good Job!'
  if (percentage >= 60) return 'Nice Try!'
  return 'Keep Practicing!'
}

const getPerformanceDescription = (percentage) => {
  if (percentage >= 90) return 'You have mastered this topic. Excellent understanding!'
  if (percentage >= 80) return 'Very good understanding. Keep up the great work!'
  if (percentage >= 70) return 'Good grasp of the material. A little more practice will help.'
  if (percentage >= 60) return 'Fair understanding. Consider reviewing the material again.'
  return 'This topic needs more attention. Review and practice more.'
}

const goToDashboard = () => {
  router.push('/dashboard')
}

const retakeQuiz = () => {
  location.reload()
}

onMounted(() => {
  loadQuiz()
})

onUnmounted(() => {
  if (timer.value) {
    clearInterval(timer.value)
  }
})
</script>

<style scoped>
.quiz-container {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.timer-display {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
  padding: 12px 20px;
  border-radius: 25px;
  font-size: 1.1rem;
  box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
}

.timer-warning {
  background: linear-gradient(135deg, #dc3545, #fd1d53) !important;
  animation: pulse 1s infinite;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.question-card {
  border-radius: 15px;
  transition: all 0.3s ease;
}

.question-text {
  line-height: 1.6;
  color: #2c3e50;
}

.option-item {
  transition: all 0.3s ease;
  border-radius: 10px;
}

.option-item:hover {
  background-color: #f8f9fa;
  transform: translateX(5px);
}

.form-check {
  padding: 0;
}

.form-check-input {
  display: none;
}

.form-check-label {
  cursor: pointer;
  margin: 0;
  padding: 15px 20px;
  border: 2px solid #e9ecef;
  border-radius: 10px;
  transition: all 0.3s ease;
}

.form-check-input:checked + .form-check-label {
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  border-color: #007bff;
  transform: scale(1.02);
}

.option-content {
  display: flex;
  align-items: center;
}

.option-letter {
  width: 35px;
  height: 35px;
  background: #6c757d;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 15px;
  flex-shrink: 0;
}

.form-check-input:checked + .form-check-label .option-letter {
  background: rgba(255, 255, 255, 0.2);
}

.option-text {
  flex: 1;
  line-height: 1.4;
}

.navigation-buttons .btn {
  min-width: 120px;
  border-radius: 25px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.navigation-buttons .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.stat-card h3 {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 5px;
}

.performance-message {
  border: none !important;
}

.action-buttons .btn {
  border-radius: 25px;
  padding: 12px 24px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.action-buttons .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
}

.progress {
  border-radius: 10px;
  overflow: hidden;
}

.progress-bar {
  transition: width 0.3s ease;
}
</style>