<template>
  <div class="subject-management">
    <div class="container-fluid py-4">
      <div class="row mb-4">
        <div class="col-12">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h2 class="mb-1">Subject Management</h2>
              <p class="text-muted mb-0">Create and manage subjects for your quizzes</p>
            </div>
            <button class="btn btn-primary" @click="showCreateModal = true">
              <i class="fas fa-plus me-2"></i>Add Subject
            </button>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-12">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-0">
              <div class="d-flex justify-content-between align-items-center">
                <h5 class="mb-0">
                  <i class="fas fa-book me-2 text-primary"></i>
                  All Subjects
                </h5>
                <div class="input-group" style="width: 300px;">
                  <span class="input-group-text">
                    <i class="fas fa-search"></i>
                  </span>
                  <input
                    type="text"
                    class="form-control"
                    placeholder="Search subjects..."
                    v-model="searchQuery"
                  >
                </div>
              </div>
            </div>
            <div class="card-body">
              <div class="row" v-if="filteredSubjects.length > 0">
                <div class="col-lg-4 col-md-6 mb-4" v-for="subject in filteredSubjects" :key="subject.id">
                  <div class="card h-100 border-0 shadow-sm subject-card">
                    <div class="card-body">
                      <div class="d-flex justify-content-between align-items-start mb-3">
                        <h5 class="card-title mb-0">{{ subject.name }}</h5>
                                                 <div class="dropdown">
                           <button class="btn btn-sm btn-outline-secondary subject-dropdown-btn" data-bs-toggle="dropdown">
                             <i class="fas fa-ellipsis-v"></i>
                           </button>
                          <ul class="dropdown-menu">
                            <li><a class="dropdown-item" href="#" @click="editSubject(subject)">
                              <i class="fas fa-edit me-2"></i>Edit
                            </a></li>
                            <li><a class="dropdown-item text-danger" href="#" @click="deleteSubject(subject.id)">
                              <i class="fas fa-trash me-2"></i>Delete
                            </a></li>
                          </ul>
                        </div>
                      </div>
                      
                      <p class="text-muted mb-3">{{ subject.description || 'No description available' }}</p>
                      
                      <div class="d-flex justify-content-between align-items-center">
                        <span class="badge bg-primary">{{ subject.chapters_count }} Chapters</span>
                        <small class="text-muted">
                          Created {{ formatDate(subject.created_at) }}
                        </small>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-5">
                <i class="fas fa-book text-muted" style="font-size: 4rem;"></i>
                <h4 class="mt-3 text-muted">No subjects found</h4>
                <p class="text-muted">Create your first subject to get started</p>
                <button class="btn btn-primary" @click="showCreateModal = true">
                  <i class="fas fa-plus me-2"></i>Add Subject
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
              <i class="fas fa-book me-2"></i>
              {{ isEditing ? 'Edit Subject' : 'Create New Subject' }}
            </h5>
            <button type="button" class="btn-close" @click="closeModal"></button>
          </div>
          <form @submit.prevent="saveSubject">
            <div class="modal-body">
              <div class="mb-3">
                <label for="subjectName" class="form-label">Subject Name *</label>
                <input
                  type="text"
                  class="form-control"
                  id="subjectName"
                  v-model="subjectForm.name"
                  required
                  placeholder="Enter subject name"
                >
              </div>
              
              <div class="mb-3">
                <label for="subjectDescription" class="form-label">Description</label>
                <textarea
                  class="form-control"
                  id="subjectDescription"
                  v-model="subjectForm.description"
                  rows="4"
                  placeholder="Enter subject description (optional)"
                ></textarea>
              </div>
            </div>
            <div class="modal-footer">
              <button type="button" class="btn btn-secondary" @click="closeModal">Cancel</button>
              <button type="submit" class="btn btn-primary" :disabled="loading">
                <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                <i v-else class="fas fa-save me-2"></i>
                {{ loading ? 'Saving...' : (isEditing ? 'Update Subject' : 'Create Subject') }}
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

interface Subject {
  id: number
  name: string
  description: string
  created_at: string
  chapters_count: number
}

interface SubjectForm {
  id: number | null
  name: string
  description: string
}

const subjects = ref<Subject[]>([])
const searchQuery = ref('')
const showCreateModal = ref(false)
const loading = ref(false)
const isEditing = ref(false)

const subjectForm = ref<SubjectForm>({
  id: null,
  name: '',
  description: ''
})

const filteredSubjects = computed(() => {
  if (!searchQuery.value) return subjects.value
  
  return subjects.value.filter(subject =>
    subject.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
    (subject.description && subject.description.toLowerCase().includes(searchQuery.value.toLowerCase()))
  )
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

const saveSubject = async () => {
  loading.value = true
  
  try {
    const token = localStorage.getItem('token')
    
    if (isEditing.value) {
      await axios.put(`http://localhost:5000/api/subjects/${subjectForm.value.id}`, {
        name: subjectForm.value.name,
        description: subjectForm.value.description
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
    } else {
      await axios.post('http://localhost:5000/api/subjects', subjectForm.value, {
        headers: { Authorization: `Bearer ${token}` }
      })
    }
    
    await loadSubjects()
    closeModal()
  } catch (error: any) {
    console.error('Error saving subject:', error)
    if (error.response?.data?.error) {
      alert(`Error: ${error.response.data.error}`)
    } else {
      alert('Error saving subject. Please try again.')
    }
  } finally {
    loading.value = false
  }
}

const editSubject = (subject: Subject) => {
  isEditing.value = true
  subjectForm.value = { ...subject }
  showCreateModal.value = true
}

const deleteSubject = async (subjectId: number) => {
  if (!confirm('Are you sure you want to delete this subject? This will also delete all associated chapters and quizzes.')) {
    return
  }
  
  try {
    const token = localStorage.getItem('token')
    await axios.delete(`http://localhost:5000/api/subjects/${subjectId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    await loadSubjects()
  } catch (error) {
    console.error('Error deleting subject:', error)
    alert('Error deleting subject. Please try again.')
  }
}

const closeModal = () => {
  showCreateModal.value = false
  isEditing.value = false
  subjectForm.value = {
    id: null,
    name: '',
    description: ''
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  })
}

onMounted(() => {
  loadSubjects()
})
</script>

<style scoped>
.subject-management {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.subject-card {
  transition: all 0.3s ease;
  cursor: pointer;
}

.subject-card:hover {
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

.form-control {
  border-radius: 8px;
  border: 1px solid #ddd;
  transition: all 0.3s ease;
}

.form-control:focus {
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

.subject-dropdown-btn {
  border: none;
  background: transparent;
  color: #6c757d;
  padding: 4px 8px;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.subject-dropdown-btn:hover {
  background-color: #f8f9fa;
  color: #495057;
  transform: scale(1.05);
}

.subject-dropdown-btn:focus {
  box-shadow: none;
  background-color: #e9ecef;
  color: #495057;
}
</style>