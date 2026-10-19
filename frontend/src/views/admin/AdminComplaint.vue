<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const activeTab = ref('owner')
const complaints = ref([])
const loading = ref(false)
const error = ref('')
const search = ref('')
const statusFilter = ref('all')

const fetchComplaints = async () => {
  try {
    loading.value = true
    error.value = ''

    const type = activeTab.value === 'owner' ? 'owner' : 'customer'

    const response = await fetch(
      `http://localhost:5000/api/admin/complaints?type=${type}`,
      {
        method: 'GET',
        headers: {
          'Authentication-Token': authStore.token
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Failed to load complaints.')
    }

    complaints.value = data.complaints || []
  } catch (err) {
    console.error('Complaints error:', err)
    error.value = err.message || 'Unable to load complaints.'
  } finally {
    loading.value = false
  }
}

const filteredComplaints = computed(() => {
  const query = search.value.trim().toLowerCase()

  return complaints.value.filter((complaint) => {
    const matchesSearch =
      !query ||
      String(complaint.id).includes(query) ||
      (complaint.complainant_name || '').toLowerCase().includes(query) ||
      (complaint.subject || '').toLowerCase().includes(query) ||
      (complaint.description || '').toLowerCase().includes(query)

    const matchesStatus =
      statusFilter.value === 'all' ||
      (complaint.status || '').toLowerCase() === statusFilter.value

    return matchesSearch && matchesStatus
  })
})

const formatDate = (value) => {
  if (!value) return 'N/A'

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) return 'N/A'

  return date.toLocaleString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const statusClass = (status) => {
  return (status || 'open').toLowerCase().replaceAll(' ', '-')
}

const changeTab = (tab) => {
  activeTab.value = tab
  search.value = ''
  statusFilter.value = 'all'
  fetchComplaints()
}

onMounted(fetchComplaints)
</script>

<template>
  <div class="complaints-page">
    <header class="page-header">
      <div>
        <p class="eyebrow">EXAMSTAY ADMIN</p>
        <h1>Complaints Management</h1>
        <p class="subtitle">
          Review complaints submitted by property owners and students.
        </p>
      </div>

      <button
        class="refresh-btn"
        @click="fetchComplaints"
        :disabled="loading"
      >
        {{ loading ? 'Loading...' : 'Refresh' }}
      </button>
    </header>

    <!-- Complaint type tabs -->
    <div class="tabs">
      <button
        :class="{ active: activeTab === 'owner' }"
        @click="changeTab('owner')"
      >
        Owner Complaints
      </button>

      <button
        :class="{ active: activeTab === 'customer' }"
        @click="changeTab('customer')"
      >
        User Complaints
      </button>
    </div>

    <!-- Summary -->
    <section class="summary-card">
      <div>
        <span>
          {{ activeTab === 'owner' ? 'Owner Complaints' : 'User Complaints' }}
        </span>
        <strong>{{ complaints.length }}</strong>
      </div>

      <div>
        <span>Open</span>
        <strong>
          {{ complaints.filter(c => (c.status || '').toLowerCase() === 'open').length }}
        </strong>
      </div>

      <div>
        <span>Resolved</span>
        <strong>
          {{ complaints.filter(c => (c.status || '').toLowerCase() === 'resolved').length }}
        </strong>
      </div>
    </section>

    <!-- Search and filter -->
    <section class="filters">
      <input
        v-model="search"
        type="text"
        placeholder="Search by ID, name, subject or description..."
      />

      <select v-model="statusFilter">
        <option value="all">All statuses</option>
        <option value="open">Open</option>
        <option value="in_progress">In Progress</option>
        <option value="resolved">Resolved</option>
        <option value="closed">Closed</option>
      </select>
    </section>

    <div v-if="loading" class="state-box">
      Loading complaints...
    </div>

    <div v-else-if="error" class="state-box error">
      <p>{{ error }}</p>
      <button class="refresh-btn" @click="fetchComplaints">
        Try Again
      </button>
    </div>

    <section v-else class="complaints-card">
      <div class="section-heading">
        <h2>
          {{ activeTab === 'owner' ? 'Owner Complaints' : 'User Complaints' }}
        </h2>
        <span>{{ filteredComplaints.length }} records</span>
      </div>

      <div v-if="filteredComplaints.length" class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>{{ activeTab === 'owner' ? 'Owner' : 'Student / User' }}</th>
              <th>Complaint</th>
              <th>Related IDs</th>
              <th>Status</th>
              <th>Submitted On</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="complaint in filteredComplaints"
              :key="complaint.id"
            >
              <td>#{{ complaint.id }}</td>

              <td>
                <strong>{{ complaint.complainant_name || 'N/A' }}</strong>
                <small>{{ complaint.email || 'N/A' }}</small>
              </td>

              <td class="complaint-description">
                <strong>{{ complaint.subject }}</strong>
                <p>{{ complaint.description }}</p>
              </td>

              <td>
                <span v-if="complaint.property_id">
                  Property: #{{ complaint.property_id }}
                </span>
                <span v-else>Property: N/A</span>

                <small>
                  Booking: {{ complaint.booking_id ?? 'N/A' }}
                </small>
              </td>

              <td>
                <span
                  class="status"
                  :class="statusClass(complaint.status)"
                >
                  {{ (complaint.status || 'open').replaceAll('_', ' ') }}
                </span>
              </td>

              <td>{{ formatDate(complaint.created_at) }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="empty-state">
        <h3>No complaints found</h3>
        <p>
          There are no complaints matching your current search and filters.
        </p>
      </div>
    </section>
  </div>
</template>

<style scoped>
.complaints-page {
  min-height: calc(100vh - 70px);
  padding: 32px;
  background: #f7f7f5;
  color: #202020;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 26px;
}

.eyebrow {
  margin: 0 0 8px;
  color: #777;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
}

h1 {
  margin: 0;
  font-size: 30px;
}

.subtitle {
  color: #737373;
  line-height: 1.5;
}

.refresh-btn {
  padding: 11px 16px;
  background: #202020;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.tabs {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  border-bottom: 1px solid #deded9;
}

.tabs button {
  padding: 13px 18px;
  background: transparent;
  border: none;
  border-bottom: 3px solid transparent;
  color: #666;
  cursor: pointer;
  font-weight: 600;
}

.tabs button.active {
  color: #202020;
  border-bottom-color: #202020;
}

.summary-card {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 18px;
  margin-bottom: 20px;
}

.summary-card > div {
  padding: 20px;
  background: white;
  border: 1px solid #e6e6e3;
  border-radius: 9px;
}

.summary-card span,
.summary-card strong {
  display: block;
}

.summary-card span {
  color: #737373;
  font-size: 13px;
}

.summary-card strong {
  margin-top: 10px;
  font-size: 27px;
}

.filters {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.filters input,
.filters select {
  min-width: 0;
  padding: 12px 14px;
  background: white;
  border: 1px solid #dcdcd7;
  border-radius: 6px;
  font-size: 14px;
}

.filters input {
  flex: 1;
}

.complaints-card {
  padding: 22px;
  background: white;
  border: 1px solid #e6e6e3;
  border-radius: 9px;
}

.section-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 20px;
}

.section-heading h2 {
  margin: 0;
  font-size: 19px;
}

.section-heading span {
  color: #777;
  font-size: 13px;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  min-width: 950px;
  border-collapse: collapse;
  text-align: left;
}

th {
  padding: 13px;
  background: #fafaf9;
  color: #686868;
  font-size: 11px;
  text-transform: uppercase;
}

td {
  padding: 15px 13px;
  border-top: 1px solid #eeeeeb;
  vertical-align: top;
  font-size: 13px;
}

td strong,
td small {
  display: block;
  overflow-wrap: anywhere;
}

td small {
  margin-top: 5px;
  color: #777;
}

.complaint-description {
  min-width: 230px;
  max-width: 350px;
}

.complaint-description p {
  margin: 7px 0 0;
  color: #666;
  line-height: 1.5;
  overflow-wrap: anywhere;
}

.status {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 20px;
  background: #fff1ce;
  color: #805b00;
  font-size: 12px;
  text-transform: capitalize;
  white-space: nowrap;
}

.status.resolved,
.status.closed {
  background: #e1f5e7;
  color: #176b35;
}

.status.in-progress {
  background: #e5edff;
  color: #254f9c;
}

.state-box,
.empty-state {
  padding: 40px 20px;
  text-align: center;
  background: white;
  border: 1px solid #e6e6e3;
  border-radius: 9px;
  color: #666;
}

.error {
  color: #a12727;
}

.empty-state h3 {
  margin: 0 0 8px;
  color: #333;
}

.empty-state p {
  margin: 0;
  font-size: 14px;
}

@media (max-width: 700px) {
  .complaints-page {
    padding: 20px 14px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .summary-card {
    gap: 8px;
  }

  .summary-card > div {
    padding: 12px;
  }

  .summary-card strong {
    font-size: 22px;
  }

  .filters {
    flex-direction: column;
  }

  .tabs button {
    padding: 12px 10px;
    font-size: 13px;
  }

  .complaints-card {
    padding: 14px;
  }
}
</style>
