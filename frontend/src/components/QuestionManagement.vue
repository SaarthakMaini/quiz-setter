<template>
  <div class="question-management">
    <div class="container-fluid py-4">
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <nav aria-label="breadcrumb">
                <ol class="breadcrumb mb-2">
                  <li class="breadcrumb-item">
                    <router-link to="/admin/quizzes" class="text-decoration-none">Quizzes</router-link>
                  </li>
                  <li class="breadcrumb-item active">{{ quiz.title }}</li>
                </ol>
              </nav>
              <h2 class="mb-1">Question Management</h2>
              <p class="text-muted mb-0">Manage questions for "{{ quiz.title }}"</p>
            </div>
            <button class="btn btn-primary" @click="showCreateModal = true">
              <i class="fas fa-plus me-2"></i>Add Question
            </button>
          </div>
        </div>
      </div>

      <div class="row mb-4">
        <div class="col-12">
          <div class="card border-0 shadow-sm">
            <div class="card-body">
              <div class="row align-items-center">
                <div class="col-md-8">
                  <h4 class="mb-2">{{ quiz.title }}</h4>
                  <div class="d-flex flex-wrap gap-2 mb-2">
                    <span class="badge bg-primary">{{ quiz.subject_name }}</span>
                    <span class="badge bg-success">{{ quiz.chapter_name }}</span>
                    <span class="badge bg-info">{{ quiz.time_duration }} minutes</span>
                    <span class="badge" :class="quiz.is_active ? 'bg-success' : 'bg-danger'">
                      {{ quiz.is_active ? 'Active' : 'Inactive' }}
                    </span>
                  </div>
                  <p class="text-muted mb-0">{{ quiz.remarks || 'No remarks' }}</p>
                </div>
                <div class="col-md-4 text-end">
                  <div class="quiz-stats">
                    <div class="stat-item">
                      <h3 class="text-primary">{{ questions.length }}</h3>
                      <small class="text-muted">Questions</small>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-12">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-0">
              <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">
                  <i class="fas fa-list me-2 text-warning"></i>
                  Questions
                </h5>
                <div class="input-group" style="width: 300px;">
                  <span class="input-group-text">
                    <i class="fas fa-search"></i>
                  </span>
                  <input
                    type="text"
                    class="form-control"
                    placeholder="Search questions..."
                    v-model="searchQuery"
                  >
                </div>
              </div>
            </div>
            <div class="card-body p-0" v-if="filteredQuestions.length > 0">
              <div class="question-item" v-for="(question, index) in filteredQuestions" :key="question.id">
                <div class="d-flex">
                  <div class="question-number">
                    <span class="badge bg-primary">{{ index + 1 }}</span>
                  </div>
                  <div class="question-content flex-grow-1">
                    <div class="d-flex justify-content-between align-items-start mb-3">
                      <h6 class="question-text mb-0">{{ question.question_statement }}</h6>
                      <div class="dropdown">
                        <button class="btn btn-sm btn-outline-secondary question-dropdown-btn" data-bs-toggle="dropdown">
                          <i class="fas fa-ellipsis-v"></i>
                        </button>
                        <ul class="dropdown-menu">
                          <li><a class="dropdown-item" href="#" @click="editQuestion(question)">
                            <i class="fas fa-edit me-2"></i>Edit
                          </a></li>
                          <li><a class="dropdown-item text-danger" href="#" @click="deleteQuestion(question.id)">
                            <i class="fas fa-trash me-2"></i>Delete
                          </a></li>
                        </ul>
                      </div>
                    </div>
                    
                    <div class="options-grid">
                      <div class="option-item" v-for="(option, optionIndex) in getOptions(question)" :key="optionIndex">
                        <div class="d-flex align-items-center">
                          <div class="option-letter" :class="{ 'correct': (optionIndex + 1) === question.correct_option }">
                            {{ String.fromCharCode(65 + optionIndex) }}
                          </div>
                          <span class="option-text" :class="{ 'fw-bold text-success': (optionIndex + 1) === question.correct_option }">
                            {{ option }}
                          </span>
                          <i v-if="(optionIndex + 1) === question.correct_option" class="fas fa-check-circle text-success ms-2"></i>
                        </div>
                      </div>
                    </div>
                    
                    <div class="question-meta mt-3">
                      <span class="badge bg-secondary">{{ question.points }} {{ question.points === 1 ? 'point' : 'points' }}</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="card-body text-center py-5">
              <i class="fas fa-question-circle text-muted" style="font-size: 4rem;"></i>
              <h4 class="mt-3 text-muted">No questions found</h4>
              <p class="text-muted">Add questions to make this quiz available to students</p>
              <button class="btn btn-primary" @click="showCreateModal = true">
                <i class="fas fa-plus me-2"></i>Add First Question
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" :class="{ show: showCreateModal }" :style="{ display: showCreateModal ? 'block' : 'none' }" tabindex="-1">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-question me-2"></i>
              {{ isEditing ? 'Edit Question' : 'Add New Question' }}
            </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <form @submit.prevent="saveQuestion">
            <div class="modal-body">
              <div class="mb-3">
                <label for="questionStatement" class="form-label">Question Statement *</label>
                <textarea
                  class="form-control"
                  id="questionStatement"
                  v-model="questionForm.question_statement"
                  required
                  rows="3"
                  placeholder="Enter your question here..."
                ></textarea>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="option1" class="form-label">Option A *</label>
                  <input
                    type="text"
                    class="form-control"
                    id="option1"
                    v-model="questionForm.option1"
                    required
                    placeholder="Enter option A"
                  >
                </div>
                
                <div class="col-md-6 mb-3">
                  <label for="option2" class="form-label">Option B *</label>
                  <input
                    type="text"
                    class="form-control"
                    id="option2"
                    v-model="questionForm.option2"
                    required
                    placeholder="Enter option B"
                  >
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="option3" class="form-label">Option C</label>
                  <input
                    type="text"
                    class="form-control"
                    id="option3"
                    v-model="questionForm.option3"
                    placeholder="Enter option C (optional)"
                  >
                </div>
                
                <div class="col-md-6 mb-3">
                  <label for="option4" class="form-label">Option D</label>
                  <input
                    type="text"
                    class="form-control"
                    id="option4"
                    v-model="questionForm.option4"
                    placeholder="Enter option D (optional)"
                  >
                </div>
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="correctOption" class="form-label">Correct Option *</label>
                  <select class="form-select" id="correctOption" v-model="questionForm.correct_option" required>
                    <option value="">Select correct option</option>
                    <option value="1">A</option>
                    <option value="2">B</option>
                    <option value="3" v-if="questionForm.option3">C</option>
                    <option value="4" v-if="questionForm.option4">D</option>
                  </select>
                </div>
                
                <div class="col-md-6 mb-3">
                  <label for="points" class="form-label">Points</label>
                  <input
                    type="number"
                    class="form-control"
                    id="points"
                    v-model="questionForm.points"
                    min="1"
                    max="10"
                    placeholder="Points for this question"
                  >
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                <i v-else class="fas fa-save me-2"></i>
                {{ loading ? 'Saving...' : (isEditing ? 'Update Question' : 'Add Question') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>

    <div v-if="showCreateModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'

interface Quiz {
  id: number
  title: string
  subject_name: string
  chapter_name: string
  time_duration: number
  remarks?: string
  is_active: boolean
}

interface Question {
  id: number
  quiz_id: number
  question_statement: string
  option1: string
  option2: string
  option3?: string
  option4?: string
  correct_option: number
  points: number
}

interface QuestionForm {
  id: number | null
  quiz_id: string | number
  question_statement: string
  option1: string
  option2: string
  option3: string
  option4: string
  correct_option: string | number
  points: number
}

const route = useRoute()
const quiz = ref<Quiz>({} as Quiz)
const questions = ref<Question[]>([])
const searchQuery = ref('')
const showCreateModal = ref(false)
const loading = ref(false)
const isEditing = ref(false)

const questionForm = ref<QuestionForm>({
  id: null,
  quiz_id: route.params.quizId as string,
  question_statement: '',
  option1: '',
  option2: '',
  option3: '',
  option4: '',
  correct_option: '',
  points: 1
})

const filteredQuestions = computed(() => {
  if (!searchQuery.value) return questions.value
  
  return questions.value.filter(question =>
    question.question_statement.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    question.option1.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    question.option2.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    (question.option3 && question.option3.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
    (question.option4 && question.option4.toLowerCase().includes(searchQuery.value.toLowerCase()))
  )
})

const loadQuiz = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://localhost:5000/api/quizzes', {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    const quizData = response.data.find((q: Quiz) => q.id === parseInt(route.params.quizId as string))
    if (quizData) {
      quiz.value = quizData
    }
  } catch (error) {
    console.error('Error loading quiz:', error)
  }
}

const loadQuestions = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`http://localhost:5000/api/quizzes/${route.params.quizId}/questions`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    questions.value = response.data
  } catch (error) {
    console.error('Error loading questions:', error)
  }
}

const getOptions = (question: Question): string[] => {
  const options = [question.option1, question.option2]
  if (question.option3) options.push(question.option3)
  if (question.option4) options.push(question.option4)
  return options
}

const saveQuestion = async () => {
  loading.value = true
  
  try {
    const token = localStorage.getItem('token')
    
    if (isEditing.value) {
      await axios.put(`http://localhost:5000/api/questions/${questionForm.value.id}`, questionForm.value, {
        headers: { Authorization: `Bearer ${token}` }
      })
    } else {
      await axios.post('http://localhost:5000/api/questions', questionForm.value, {
        headers: { Authorization: `Bearer ${token}` }
      })
    }
    
    await loadQuestions()
    closeModal()
  } catch (error) {
    console.error('Error saving question:', error)
    alert('Error saving question. Please try again.')
  } finally {
    loading.value = false
  }
}

const editQuestion = (question: Question) => {
  isEditing.value = true
  questionForm.value = {
    id: question.id,
    quiz_id: String(question.quiz_id),
    question_statement: question.question_statement,
    option1: question.option1,
    option2: question.option2,
    option3: question.option3 || '',
    option4: question.option4 || '',
    correct_option: String(question.correct_option),
    points: question.points
  }
  showCreateModal.value = true
}

const deleteQuestion = async (questionId: number) => {
  if (!confirm('Are you sure you want to delete this question?')) {
    return
  }
  
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://localhost:5000/api/questions/${questionId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    await loadQuestions()
  } catch (error) {
    console.error('Error deleting question:', error)
    alert('Error deleting question. Please try again.')
  }
}

const closeModal = () => {
  showCreateModal.value = false
  isEditing.value = false
  questionForm.value = {
    id: null,
    quiz_id: route.params.quizId as string,
    question_statement: '',
    option1: '',
    option2: '',
    option3: '',
    option4: '',
    correct_option: '',
    points: 1
  }
}

onMounted(async () => {
  await loadQuiz()
  await loadQuestions()
})
</script>

<style scoped>
.question-management {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.quiz-stats {
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
}

.stat-item h3 {
  color: white;
  margin-bottom: 5px;
}

.question-item {
  padding: 20px;
  border-bottom: 1px solid #e9ecef;
  transition: all 0.3s ease;
}

.question-item:hover {
  background-color: #f8f9fa;
}

.question-item:last-child {
  border-bottom: none;
}

.question-number {
  margin-right: 15px;
  flex-shrink: 0;
}

.question-number .badge {
  width: 35px;
  height: 35px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  font-weight: bold;
}

.question-text {
  font-size: 1.1rem;
  line-height: 1.5;
  color: #2c3e50;
}

.options-grid {
  display: grid;
  gap: 10px;
  margin-top: 15px;
}

.option-item {
  background: #f8f9fa;
  padding: 10px 15px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.option-item:hover {
  background: #e9ecef;
}

.option-letter {
  width: 25px;
  height: 25px;
  background: #6c757d;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 0.8rem;
  margin-right: 10px;
  flex-shrink: 0;
}

.option-letter.correct {
  background: #28a745;
}

.option-text {
  flex: 1;
}

.question-meta {
  padding-top: 10px;
  border-top: 1px solid #e9ecef;
}

.card {
  border-radius: 12px;
}

.modal-content {
  border-radius: 12px;
  border: none;
}

.modal-header {
  border-bottom: 1px solid #e9ecef;
  border-radius: 12px 12px 0 0;
}

.form-control, .form-select {
  border-radius: 8px;
  border: 1px solid #ddd;
  transition: all 0.3s ease;
}

.form-control:focus, .form-select:focus {
  box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.15);
  border-color: #86b7fe;
  transform: translateY(-1px);
}

.btn {
  border-radius: 8px;
  font-weight: 500;
  transition: all 0.3s ease;
}

.btn:hover {
  transform: translateY(-1px);
}

.btn-primary:hover {
  box-shadow: 0 4px 12px rgba(0, 123, 255, 0.3);
}

.breadcrumb {
  background: transparent;
  padding: 0;
}

.breadcrumb-item + .breadcrumb-item::before {
  content: ">";
  color: #6c757d;
}

.dropdown-menu {
  border: none;
  box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
  border-radius: 8px;
}

.dropdown-item {
  transition: all 0.3s ease;
}

.dropdown-item:hover {
  background-color: #f8f9fa;
  transform: translateX(5px);
}

.input-group-text {
  background: transparent;
  border: 1px solid #ddd;
}

.badge {
  font-size: 0.75rem;
  padding: 6px 12px;
  border-radius: 15px;
}

.question-dropdown-btn {
  background: transparent !important;
  border: none !important;
  padding: 0.25rem 0.5rem;
  color: #6c757d;
  transition: all 0.3s ease;
}

.question-dropdown-btn:hover,
.question-dropdown-btn:focus {
  background: rgba(108, 117, 125, 0.1) !important;
  color: #495057;
  box-shadow: none !important;
}

.question-dropdown-btn::after {
  display: none !important;
}
</style>