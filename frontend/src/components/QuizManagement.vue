<template>
  <div class="quiz-management">
    <div class="container-fluid py-4">
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h2 class="mb-1">Quiz Management</h2>
              <p class="text-muted mb-0">Create and manage quizzes for your chapters</p>
            </div>
            <button class="btn btn-primary" @click="showCreateModal = true">
              <i class="fas fa-plus me-2"></i>Create Quiz
            </button>
          </div>
        </div>
      </div>

      <div class="row mb-4">
        <div class="col-md-4">
          <div class="input-group">
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
        <div class="col-md-4">
          <select class="form-select" v-model="selectedSubject" @change="filterBySubject">
            <option value="">All Subjects</option>
            <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
              {{ subject.name }}
            </option>
          </select>
        </div>
        <div class="col-md-4">
          <select class="form-select" v-model="selectedChapter">
            <option value="">All Chapters</option>
            <option v-for="chapter in filteredChaptersList" :key="chapter.id" :value="chapter.id">
              {{ chapter.name }}
            </option>
          </select>
        </div>
      </div>

      <div class="row">
        <div class="col-12">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-0">
              <h5 class="mb-0">
                <i class="fas fa-question-circle me-2 text-warning"></i>
                All Quizzes
              </h5>
            </div>
            <div class="card-body">
              <div class="row" v-if="filteredQuizzes.length > 0">
                <div class="col-lg-4 col-md-6 mb-4" v-for="quiz in filteredQuizzes" :key="quiz.id">
                  <div class="card h-100 border-0 shadow-sm quiz-card">
                    <div class="card-body">
                      <div class="d-flex justify-content-between align-items-start mb-3">
                        <h5 class="card-title mb-0">{{ quiz.title }}</h5>
                        <div class="dropdown">
                          <button class="btn btn-sm btn-outline-secondary quiz-dropdown-btn" data-bs-toggle="dropdown">
                            <i class="fas fa-ellipsis-v"></i>
                          </button>
                          <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#" @click="editQuiz(quiz)">
                              <i class="fas fa-edit me-2"></i>Edit Quiz
                            </a></li>
                            <li><a class="dropdown-item" href="#" @click="manageQuestions(quiz.id)">
                              <i class="fas fa-list me-2"></i>Manage Questions
                            </a></li>
                            <li><a class="dropdown-item" href="#" @click="toggleQuizStatus(quiz)">
                              <i class="fas fa-toggle-on me-2"></i>{{ quiz.is_active ? 'Deactivate' : 'Activate' }}
                            </a></li>
                            <li><hr class="dropdown-divider"></li>
                            <li><a class="dropdown-item text-danger" href="#" @click="deleteQuiz(quiz.id)">
                              <i class="fas fa-trash me-2"></i>Delete
                            </a></li>
                          </ul>
                        </div>
                      </div>
                      
                      <div class="mb-3">
                        <span class="badge bg-primary me-2">{{ quiz.subject_name }}</span>
                        <span class="badge bg-success">{{ quiz.chapter_name }}</span>
                      </div>
                      
                      <div class="quiz-info mb-3">
                        <div class="d-flex justify-content-between mb-2">
                          <span class="text-muted small">
                            <i class="fas fa-question me-1"></i>{{ quiz.questions_count }} Questions
                          </span>
                          <span class="text-muted small">
                            <i class="fas fa-clock me-1"></i>{{ quiz.time_duration }} mins
                          </span>
                        </div>
                        <div class="d-flex justify-content-between mb-2">
                          <span class="text-muted small">
                            <i class="fas fa-users me-1"></i>{{ quiz.attempts_count }} Attempts
                          </span>
                          <span class="small" :class="quiz.is_active ? 'text-success' : 'text-danger'">
                            <i class="fas fa-circle me-1"></i>{{ quiz.is_active ? 'Active' : 'Inactive' }}
                          </span>
                        </div>
                      </div>
                      
                      <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">
                          {{ formatDate(quiz.date_of_quiz) }}
                        </small>
                        <button class="btn btn-sm btn-primary" @click="manageQuestions(quiz.id)">
                          <i class="fas fa-cog me-1"></i>Manage
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-5">
                <i class="fas fa-question-circle text-muted" style="font-size: 4rem;"></i>
                <h4 class="mt-3 text-muted">No quizzes found</h4>
                <p class="text-muted">Create your first quiz to get started</p>
                <button class="btn btn-primary" @click="showCreateModal = true">
                  <i class="fas fa-plus me-2"></i>Create Quiz
                </button>
              </div>
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
              <i class="fas fa-question-circle me-2"></i>
              {{ isEditing ? 'Edit Quiz' : 'Create New Quiz' }}
            </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <form @submit.prevent="saveQuiz">
            <div class="modal-body">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="quizSubject" class="form-label">Subject *</label>
                  <select class="form-select" id="quizSubject" v-model="quizForm.subject_id" @change="loadChaptersForSubject" required>
                    <option value="">Select a subject</option>
                    <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                      {{ subject.name }}
                    </option>
                  </select>
                </div>
                
                <div class="col-md-6 mb-3">
                  <label for="quizChapter" class="form-label">Chapter *</label>
                  <select class="form-select" id="quizChapter" v-model="quizForm.chapter_id" required>
                    <option value="">Select a chapter</option>
                    <option v-for="chapter in chaptersForForm" :key="chapter.id" :value="chapter.id">
                      {{ chapter.name }}
                    </option>
                  </select>
                </div>
              </div>
              
              <div class="mb-3">
                <label for="quizTitle" class="form-label">Quiz Title *</label>
                <input
                  type="text"
                  class="form-control"
                  id="quizTitle"
                  v-model="quizForm.title"
                  required
                  placeholder="Enter quiz title"
                >
              </div>
              
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="quizDate" class="form-label">Quiz Date *</label>
                  <input
                    type="datetime-local"
                    class="form-control"
                    id="quizDate"
                    v-model="quizForm.date_of_quiz"
                    required
                  >
                </div>
                
                <div class="col-md-6 mb-3">
                  <label for="quizDuration" class="form-label">Duration (minutes) *</label>
                  <input
                    type="number"
                    class="form-control"
                    id="quizDuration"
                    v-model="quizForm.time_duration"
                    required
                    min="1"
                    max="180"
                    placeholder="Duration in minutes"
                  >
                </div>
              </div>
              
              <div class="mb-3">
                <label for="quizRemarks" class="form-label">Remarks</label>
                <textarea
                  class="form-control"
                  id="quizRemarks"
                  v-model="quizForm.remarks"
                  rows="3"
                  placeholder="Enter quiz instructions or remarks (optional)"
                ></textarea>
              </div>
              
              <div class="form-check">
                <input
                  class="form-check-input"
                  type="checkbox"
                  id="quizActive"
                  v-model="quizForm.is_active"
                >
                <label class="form-check-label" for="quizActive">
                  Make quiz active immediately
                </label>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                <i v-else class="fas fa-save me-2"></i>
                {{ loading ? 'Saving...' : (isEditing ? 'Update Quiz' : 'Create Quiz') }}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <!-- Modal Backdrop -->
    <div v-if="showCreateModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

interface Quiz {
  id: number
  title: string
  chapter_id: number
  subject_id: number
  date_of_quiz: string
  time_duration: number
  remarks: string
  is_active: boolean
  subject_name: string
  chapter_name: string
  questions_count: number
  attempts_count: number
  chapter?: {
    id: number
    subject_id: number
  }
}

interface Subject {
  id: number
  name: string
  description: string
  created_at: string
  chapters_count: number
}

interface Chapter {
  id: number
  name: string
  description: string
  subject_id: number
  subject_name: string
  created_at: string
  quizzes_count: number
}

interface QuizForm {
  id: number | null
  title: string
  chapter_id: string
  subject_id: string
  date_of_quiz: string
  time_duration: number
  remarks: string
  is_active: boolean
}

const router = useRouter()
const quizzes = ref<Quiz[]>([])
const subjects = ref<Subject[]>([])
const chapters = ref<Chapter[]>([])
const chaptersForForm = ref<Chapter[]>([])
const searchQuery = ref('')
const selectedSubject = ref('')
const selectedChapter = ref('')
const showCreateModal = ref(false)
const loading = ref(false)
const isEditing = ref(false)

const quizForm = ref<QuizForm>({
  id: null,
  title: '',
  chapter_id: '',
  subject_id: '',
  date_of_quiz: '',
  time_duration: 60,
  remarks: '',
  is_active: true
})

const filteredChaptersList = computed(() => {
  if (!selectedSubject.value) return chapters.value
  return chapters.value.filter(chapter => chapter.subject_id === parseInt(selectedSubject.value))
})

const filteredQuizzes = computed(() => {
  let filtered = quizzes.value
  
  if (searchQuery.value) {
    filtered = filtered.filter(quiz =>
      quiz.title.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      quiz.subject_name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      quiz.chapter_name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
  }
  
  if (selectedChapter.value) {
    filtered = filtered.filter(quiz => quiz.chapter_id === parseInt(selectedChapter.value))
  }
  
  return filtered
})

const loadSubjects = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://localhost:5000/api/subjects', {
      headers: { Authorization: `Bearer ${token}` }
    })
    subjects.value = response.data
  } catch (error) {
    console.error('Error loading subjects:', error)
  }
}

const loadAllChapters = async () => {
  try {
    const token = localStorage.getItem('token')
    let allChapters: Chapter[] = []
    
    for (const subject of subjects.value) {
      const response = await axios.get(`http://localhost:5000/api/subjects/${subject.id}/chapters`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      allChapters = [...allChapters, ...response.data]
    }
    
    chapters.value = allChapters
  } catch (error) {
    console.error('Error loading chapters:', error)
  }
}

const loadChaptersForSubject = async () => {
  if (!quizForm.value.subject_id) {
    chaptersForForm.value = []
    return
  }
  
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get(`http://localhost:5000/api/subjects/${quizForm.value.subject_id}/chapters`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    chaptersForForm.value = response.data
  } catch (error) {
    console.error('Error loading chapters for subject:', error)
    chaptersForForm.value = []
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

const filterBySubject = () => {
  selectedChapter.value = ''
}

const saveQuiz = async () => {
  loading.value = true
  
  try {
    const token = localStorage.getItem('token')
    
    if (isEditing.value) {
      await axios.put(`http://localhost:5000/api/quizzes/${quizForm.value.id}`, {
        title: quizForm.value.title,
        chapter_id: parseInt(quizForm.value.chapter_id),
        date_of_quiz: quizForm.value.date_of_quiz,
        time_duration: quizForm.value.time_duration,
        remarks: quizForm.value.remarks,
        is_active: quizForm.value.is_active
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
    } else {
      await axios.post('http://localhost:5000/api/quizzes', {
        title: quizForm.value.title,
        chapter_id: parseInt(quizForm.value.chapter_id),
        date_of_quiz: quizForm.value.date_of_quiz,
        time_duration: quizForm.value.time_duration,
        remarks: quizForm.value.remarks,
        is_active: quizForm.value.is_active
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
    }
    
    await loadQuizzes()
    closeModal()
  } catch (error: any) {
    console.error('Error saving quiz:', error)
    if (error.response?.data?.error) {
      alert(`Error: ${error.response.data.error}`)
    } else {
      alert('Error saving quiz. Please try again.')
    }
  } finally {
    loading.value = false
  }
}

const editQuiz = async (quiz: Quiz) => {
  isEditing.value = true
  
  const chapter = chapters.value.find(c => c.id === quiz.chapter_id)
  const subject_id = chapter ? String(chapter.subject_id) : ''
  
  quizForm.value = {
    id: quiz.id as number | null,
    title: quiz.title,
    chapter_id: String(quiz.chapter_id),
    subject_id: subject_id,
    date_of_quiz: new Date(quiz.date_of_quiz).toISOString().slice(0, 16),
    time_duration: quiz.time_duration,
    remarks: quiz.remarks,
    is_active: quiz.is_active
  }
  
  await loadChaptersForSubject()
  
  showCreateModal.value = true
}

const manageQuestions = (quizId: number) => {
  router.push(`/admin/questions/${quizId}`)
}

const toggleQuizStatus = async (quiz: Quiz) => {
  try {
    const token = localStorage.getItem('token')
    await axios.patch(`http://localhost:5000/api/quizzes/${quiz.id}`, {
      is_active: !quiz.is_active
    }, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    await loadQuizzes()
  } catch (error) {
    console.error('Error updating quiz status:', error)
    alert('Error updating quiz status. Please try again.')
  }
}

const deleteQuiz = async (quizId: number) => {
  if (!confirm('Are you sure you want to delete this quiz? This action cannot be undone.')) {
    return
  }
  
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://localhost:5000/api/quizzes/${quizId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    await loadQuizzes()
  } catch (error) {
    console.error('Error deleting quiz:', error)
    alert('Error deleting quiz. Please try again.')
  }
}

const closeModal = () => {
  showCreateModal.value = false
  isEditing.value = false
  quizForm.value = {
    id: null,
    title: '',
    chapter_id: '',
    subject_id: '',
    date_of_quiz: '',
    time_duration: 60,
    remarks: '',
    is_active: true
  }
  chaptersForForm.value = []
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(async () => {
  await loadSubjects()
  await loadAllChapters()
  await loadQuizzes()
})
</script>

<style scoped>
.quiz-management {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.quiz-card {
  transition: all 0.3s ease;
  cursor: pointer;
}

.quiz-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
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

.quiz-info {
  background-color: #f8f9fa;
  padding: 12px;
  border-radius: 8px;
}

.badge {
  font-size: 0.75rem;
  padding: 6px 12px;
  border-radius: 15px;
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

.form-check-input:checked {
  background-color: #007bff;
  border-color: #007bff;
}

.quiz-dropdown-btn {
  border: none;
  background: transparent;
  color: #6c757d;
  padding: 4px 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.quiz-dropdown-btn::after {
  display: none !important;
}

.quiz-dropdown-btn:hover {
  background-color: #f8f9fa;
  color: #495057;
  transform: scale(1.05);
}

.quiz-dropdown-btn:focus {
  box-shadow: none;
  background-color: #e9ecef;
  color: #495057;
}
</style>