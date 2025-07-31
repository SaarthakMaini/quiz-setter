<template>
  <div class="admin-dashboard">
    <div class="container-fluid py-4">
      <div class="row mb-4">
        <div class="col-12">
          <div class="card bg-gradient-primary text-white border-0">
            <div class="card-body">
              <div class="row align-items-center">
                <div class="col-md-8">
                  <h2 class="mb-1">Admin Dashboard</h2>
                  <p class="mb-0 opacity-75">Manage your quiz platform and monitor user activity</p>
                </div>
                <div class="col-md-4 text-end">
                  <i class="fas fa-crown" style="font-size: 4rem; opacity: 0.3;"></i>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="row mb-4">
        <div class="col-lg-3 col-md-6 mb-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body text-center">
              <div class="stat-icon bg-primary text-white mb-3">
                <i class="fas fa-users fa-2x"></i>
              </div>
              <h3 class="fw-bold text-primary">{{ stats.total_users || 0 }}</h3>
              <p class="text-muted mb-0">Total Users</p>
            </div>
          </div>
        </div>
        
        <div class="col-lg-3 col-md-6 mb-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body text-center">
              <div class="stat-icon bg-success text-white mb-3">
                <i class="fas fa-book fa-2x"></i>
              </div>
              <h3 class="fw-bold text-success">{{ stats.total_subjects || 0 }}</h3>
              <p class="text-muted mb-0">Subjects</p>
            </div>
          </div>
        </div>
        
        <div class="col-lg-3 col-md-6 mb-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body text-center">
              <div class="stat-icon bg-warning text-white mb-3">
                <i class="fas fa-question-circle fa-2x"></i>
              </div>
              <h3 class="fw-bold text-warning">{{ stats.total_quizzes || 0 }}</h3>
              <p class="text-muted mb-0">Total Quizzes</p>
            </div>
          </div>
        </div>
        
        <div class="col-lg-3 col-md-6 mb-3">
          <div class="card border-0 shadow-sm h-100">
            <div class="card-body text-center">
              <div class="stat-icon bg-info text-white mb-3">
                <i class="fas fa-clipboard-check fa-2x"></i>
              </div>
              <h3 class="fw-bold text-info">{{ stats.total_attempts || 0 }}</h3>
              <p class="text-muted mb-0">Quiz Attempts</p>
            </div>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-lg-8 mb-4">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-0 pb-0">
              <h5 class="mb-0">
                <i class="fas fa-bolt text-warning me-2"></i>
                Quick Actions
              </h5>
            </div>
            <div class="card-body">
              <div class="row">
                <div class="col-md-6 mb-3">
                  <router-link to="/admin/subjects" class="action-card text-decoration-none">
                    <div class="card border-0 h-100 action-item">
                      <div class="card-body text-center">
                        <div class="action-icon bg-primary text-white mb-3">
                          <i class="fas fa-book-open fa-2x"></i>
                        </div>
                        <h6 class="card-title">Manage Subjects</h6>
                        <p class="text-muted small">Create and organize subjects</p>
                      </div>
                    </div>
                  </router-link>
                </div>
                
                <div class="col-md-6 mb-3">
                  <router-link to="/admin/chapters" class="action-card text-decoration-none">
                    <div class="card border-0 h-100 action-item">
                      <div class="card-body text-center">
                        <div class="action-icon bg-success text-white mb-3">
                          <i class="fas fa-bookmark fa-2x"></i>
                        </div>
                        <h6 class="card-title">Manage Chapters</h6>
                        <p class="text-muted small">Add chapters to subjects</p>
                      </div>
                    </div>
                  </router-link>
                </div>
                
                <div class="col-md-6 mb-3">
                  <router-link to="/admin/quizzes" class="action-card text-decoration-none">
                    <div class="card border-0 h-100 action-item">
                      <div class="card-body text-center">
                        <div class="action-icon bg-warning text-white mb-3">
                          <i class="fas fa-question-circle fa-2x"></i>
                        </div>
                        <h6 class="card-title">Manage Quizzes</h6>
                        <p class="text-muted small">Create and edit quizzes</p>
                      </div>
                    </div>
                  </router-link>
                </div>
                
                <div class="col-md-6 mb-3">
                  <div class="action-card">
                    <div class="card border-0 h-100 action-item" @click="exportData">
                      <div class="card-body text-center">
                        <div class="action-icon bg-info text-white mb-3">
                          <i class="fas fa-download fa-2x"></i>
                        </div>
                        <h6 class="card-title">Export Data</h6>
                        <p class="text-muted small">Download quiz data as CSV</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="col-lg-4">
          <div class="card border-0 shadow-sm">
            <div class="card-header bg-white border-0 pb-0">
              <h5 class="mb-0">
                <i class="fas fa-clock text-primary me-2"></i>
                Recent Activity
              </h5>
            </div>
            <div class="card-body">
              <div v-if="stats.recent_attempts && stats.recent_attempts.length > 0">
                <div
                  class="activity-item d-flex align-items-center mb-3 p-2 rounded"
                  v-for="attempt in stats.recent_attempts.slice(0, 8)"
                  :key="attempt.id"
                >
                  <div class="flex-shrink-0 me-3">
                    <div class="activity-avatar">
                      <i class="fas fa-user"></i>
                    </div>
                  </div>
                  <div class="flex-grow-1">
                    <h6 class="mb-1 small">{{ attempt.user_name }}</h6>
                    <p class="text-muted small mb-0">
                      Completed "{{ attempt.quiz_title }}" - {{ Math.round(attempt.percentage) }}%
                    </p>
                    <small class="text-muted">
                      {{ formatDate(attempt.timestamp_of_attempt) }}
                    </small>
                  </div>
                </div>
              </div>
              <div v-else class="text-center py-4">
                <i class="fas fa-inbox text-muted" style="font-size: 2rem;"></i>
                <p class="text-muted mt-2">No recent activity</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const router = useRouter()
const stats = ref({})

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

const exportData = async () => {
  try {
    const token = localStorage.getItem('token')
    
    alert('CSV export has been initiated. You will receive an email when ready.')
    
    const response = await axios.post('http://localhost:5000/api/tasks/export_admin_quiz_data', {}, {
      headers: { Authorization: `Bearer ${token}` }
    })
    
    console.log('Export response:', response.data)
    
  } catch (error) {
    console.error('Error exporting data:', error)
    alert('Error exporting data. Please try again.')
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped>
.admin-dashboard {
  background-color: #f8f9fa;
  min-height: 100vh;
}

.bg-gradient-primary {
  background: linear-gradient(135deg, #007bff, #0056b3);
}

.stat-icon {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.action-card {
  display: block;
  text-decoration: none;
  color: inherit;
}

.action-item {
  transition: all 0.3s ease;
  cursor: pointer;
  border: 2px solid transparent;
}

.action-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  border-color: #e9ecef;
}

.action-icon {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto;
}

.activity-item {
  background-color: #f8f9fa;
  transition: all 0.3s ease;
}

.activity-item:hover {
  background-color: #e9ecef;
}

.activity-avatar {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #6c757d, #495057);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.card {
  border-radius: 12px;
}

.card-header {
  border-radius: 12px 12px 0 0;
}
</style>