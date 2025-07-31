<template>
  <div class="chapter-management">
    <div class="container-fluid py-4">
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h2 class="mb-1">Chapter Management</h2>
              <p class="text-muted mb-0">Organize chapters within subjects</p>
            </div>
            <button class="btn btn-primary" @click="showCreateModal = true">
              <i class="fas fa-plus me-2"></i>Add Chapter
            </button>
          </div>
        </div>
      </div>

      <div class="row mb-4">
        <div class="col-md-6">
          <div class="input-group">
            <span class="input-group-text">
              <i class="fas fa-search"></i>
            </span>
            <input
              type="text"
              class="form-control"
              placeholder="Search chapters..."
              v-model="searchQuery"
            >
          </div>
        </div>
        <div class="col-md-6">
          <select class="form-select" v-model="selectedSubject" @change="loadChapters">
            <option value="">All Subjects</option>
            <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
              {{ subject.name }}
            </option>
          </select>
        </div>
      </div>

      <div class="row">
        <div class="col-12">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-0">
              <h5 class="mb-0">
                <i class="fas fa-bookmark me-2 text-success"></i>
                Chapters
              </h5>
            </div>
            <div class="card-body p-0">
              <div class="table-responsive">
                <table class="table table-hover mb-0" v-if="filteredChapters.length > 0">
                  <thead class="table-light">
                    <tr>
                      <th>Chapter Name</th>
                      <th>Subject</th>
                      <th>Description</th>
                      <th>Quizzes</th>
                      <th>Created</th>
                      <th>Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="chapter in filteredChapters" :key="chapter.id" class="chapter-row">
                      <td>
                        <div class="fw-bold">{{ chapter.name }}</div>
                      </td>
                      <td>
                        <span class="badge bg-primary">{{ chapter.subject_name }}</span>
                      </td>
                      <td>
                        <span class="text-muted">{{ chapter.description || 'No description' }}</span>
                      </td>
                      <td>
                        <span class="badge bg-info">{{ chapter.quizzes_count }} quizzes</span>
                      </td>
                      <td>
                        <small class="text-muted">{{ formatDate(chapter.created_at) }}</small>
                      </td>
                      <td>
                        <div class="btn-group btn-group-sm">
                          <button class="btn btn-outline-primary" @click="editChapter(chapter)">
                            <i class="fas fa-edit"></i>
                          </button>
                          <button class="btn btn-outline-danger" @click="deleteChapter(chapter.id)">
                            <i class="fas fa-trash"></i>
                          </button>
                        </div>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-if="filteredChapters.length === 0" class="text-center py-5">
                <i class="fas fa-bookmark text-muted" style="font-size: 4rem;"></i>
                <h4 class="mt-3 text-muted">No chapters found</h4>
                <p class="text-muted">Create your first chapter to organize quizzes</p>
                <button class="btn btn-primary" @click="showCreateModal = true">
                  <i class="fas fa-plus me-2"></i>Add Chapter
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" :class="{ show: showCreateModal }" :style="{ display: showCreateModal ? 'block' : 'none' }" tabindex="-1">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i class="fas fa-bookmark me-2"></i>
              {{ isEditing ? 'Edit Chapter' : 'Create New Chapter' }}
            </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <form @submit.prevent="saveChapter">
            <div class="modal-body">
              <div class="mb-3">
                <label for="chapterSubject" class="form-label">Subject *</label>
                <select class="form-select" id="chapterSubject" v-model="chapterForm.subject_id" required>
                  <option value="">Select a subject</option>
                  <option v-for="subject in subjects" :key="subject.id" :value="subject.id">
                    {{ subject.name }}
                  </option>
                </select>
              </div>
              
              <div class="mb-3">
                <label for="chapterName" class="form-label">Chapter Name *</label>
                <input
                  type="text"
                  class="form-control"
                  id="chapterName"
                  v-model="chapterForm.name"
                  required
                  placeholder="Enter chapter name"
                >
              </div>
              
              <div class="mb-3">
                <label for="chapterDescription" class="form-label">Description</label>
                <textarea
                  class="form-control"
                  id="chapterDescription"
                  v-model="chapterForm.description"
                  rows="4"
                  placeholder="Enter chapter description (optional)"
                ></textarea>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                <i v-else class="fas fa-save me-2"></i>
                {{ loading ? 'Saving...' : (isEditing ? 'Update Chapter' : 'Create Chapter') }}
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
import axios from 'axios'

interface Chapter {
  id: number
  name: string
  description: string
  subject_id: number
  subject_name: string
  created_at: string
  quizzes_count: number
}

interface Subject {
  id: number
  name: string
  description: string
  created_at: string
  chapters_count: number
}

interface ChapterForm {
  id: number | null
  name: string
  description: string
  subject_id: string | number
}

const chapters = ref<Chapter[]>([])
const subjects = ref<Subject[]>([])
const searchQuery = ref('')
const selectedSubject = ref('')
const showCreateModal = ref(false)
const loading = ref(false)
const isEditing = ref(false)

const chapterForm = ref<ChapterForm>({
  id: null,
  name: '',
  description: '',
  subject_id: ''
})

const filteredChapters = computed(() => {
  let filtered = chapters.value
  
  if (searchQuery.value) {
    filtered = filtered.filter(chapter =>
      chapter.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      (chapter.description && chapter.description.toLowerCase().includes(searchQuery.value.toLowerCase())) ||
      chapter.subject_name.toLowerCase().includes(searchQuery.value.toLowerCase())
    )
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

const loadChapters = async () => {
  try {
    const token = localStorage.getItem('token')
    let allChapters: Chapter[] = []
    
    if (selectedSubject.value) {
      const response = await axios.get(`http://localhost:5000/api/subjects/${selectedSubject.value}/chapters`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      allChapters = response.data
    } else {
      for (const subject of subjects.value) {
        const response = await axios.get(`http://localhost:5000/api/subjects/${subject.id}/chapters`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        allChapters = [...allChapters, ...response.data]
      }
    }
    
    chapters.value = allChapters
  } catch (error) {
    console.error('Error loading chapters:', error)
  }
}

const saveChapter = async () => {
  loading.value = true
  
  try {
    const token = localStorage.getItem('token')
    
    if (isEditing.value) {
      await axios.put(`http://localhost:5000/api/chapters/${chapterForm.value.id}`, {
        name: chapterForm.value.name,
        description: chapterForm.value.description
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
    } else {
      // Create new chapter
      await axios.post('http://localhost:5000/api/chapters', chapterForm.value, {
        headers: { Authorization: `Bearer ${token}` }
      })
    }
    
    await loadChapters()
    closeModal()
  } catch (error: any) {
    console.error('Error saving chapter:', error)
    if (error.response?.data?.error) {
      alert(`Error: ${error.response.data.error}`)
    } else {
      alert('Error saving chapter. Please try again.')
    }
  } finally {
    loading.value = false
  }
}

const editChapter = (chapter: Chapter) => {
  isEditing.value = true
  chapterForm.value = { ...chapter }
  showCreateModal.value = true
}

const deleteChapter = async (chapterId: number) => {
  if (!confirm('Are you sure you want to delete this chapter? This will also delete all associated quizzes.')) {
    return
  }
  
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://localhost:5000/api/chapters/${chapterId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    await loadChapters()
  } catch (error) {
    console.error('Error deleting chapter:', error)
    alert('Error deleting chapter. Please try again.')
  }
}

const closeModal = () => {
  showCreateModal.value = false
  isEditing.value = false
  chapterForm.value = {
    id: null,
    name: '',
    description: '',
    subject_id: ''
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

onMounted(async () => {
  await loadSubjects()
  await loadChapters()
})
</script>

<style scoped>
.chapter-management {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.chapter-row {
  transition: all 0.3s ease;
}

.chapter-row:hover {
  background-color: #f8f9fa;
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

.table {
  font-size: 0.9rem;
}

.table th {
  font-weight: 600;
  color: #495057;
  border-bottom: 2px solid #dee2e6;
}

.badge {
  font-size: 0.75rem;
  padding: 6px 12px;
  border-radius: 15px;
}

.input-group-text {
  background: transparent;
  border: 1px solid #ddd;
}

.btn-group-sm .btn {
  padding: 4px 8px;
  font-size: 0.875rem;
}
</style>