
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const properties = ref([])
const totalPending = ref(0)
const search = ref('')
const loading = ref(false)
const error = ref('')

let searchTimer = null

const fetchPendingProperties = async () => {
  try {
    loading.value = true
    error.value = ''

    const params = new URLSearchParams()

    if (search.value.trim()) {
      params.set('search', search.value.trim())
    }

    const response = await fetch(
      `http://localhost:5000/api/admin/verifications?${params.toString()}`,
      {
        method: 'GET',
        headers: {
          'Authentication-Token': authStore.token
        }
      }
    )

    const text = await response.text()
    let data

    try {
      data = JSON.parse(text)
    } catch {
      throw new Error(
        `Invalid server response. HTTP ${response.status}. Check API route or authentication.`
      )
    }

    if (!response.ok) {
      throw new Error(
        data.message || 'Failed to fetch pending verifications.'
      )
    }

    properties.value = data.properties || []
    totalPending.value = data.total_pending || 0

  } catch (err) {
    console.error('Verification API error:', err)
    error.value = err.message || 'Unable to load pending verifications.'
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(fetchPendingProperties, 400)
}

const clearSearch = () => {
  search.value = ''
  fetchPendingProperties()
}

const viewProperty = (id) => {
  router.push(`/admin/properties/${id}`)
}

const formatDate = (value) => {
  if (!value) return 'N/A'

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) return 'N/A'

  return date.toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

onMounted(fetchPendingProperties)

onUnmounted(() => {
  clearTimeout(searchTimer)
})
</script>

<template>
  <div class="verification-page">

    <header class="page-header">
      <div>
        <p class="eyebrow">EXAMSTAY ADMIN</p>
        <h1>Property Verification</h1>
        <p class="subtitle">
          Review properties awaiting verification.
        </p>
      </div>

      <button
        class="secondary-btn"
        :disabled="loading"
        @click="fetchPendingProperties"
      >
        ↻ Refresh
      </button>
    </header>

    <section class="summary-card">
      <div>
        <span>Pending properties</span>
        <strong>{{ totalPending }}</strong>
      </div>
      <span class="pending-badge">Awaiting review</span>
    </section>

    <section class="search-bar">
      <span class="search-icon">⌕</span>

      <input
        v-model="search"
        type="text"
        placeholder="Search property, owner, city, address or email..."
        @input="handleSearch"
      />

      <button
        v-if="search"
        class="clear-btn"
        @click="clearSearch"
      >
        Clear
      </button>
    </section>

    <div v-if="loading" class="state-box">
      Loading pending properties...
    </div>

    <div v-else-if="error" class="state-box error">
      <p>{{ error }}</p>
      <button class="secondary-btn" @click="fetchPendingProperties">
        Try Again
      </button>
    </div>

    <div v-else-if="properties.length === 0" class="state-box">
      <h3>No pending properties found</h3>
      <p>
        {{
          search
            ? 'Try another property or owner name.'
            : 'All properties have been reviewed.'
        }}
      </p>
    </div>

    <template v-else>
      <div class="list-heading">
        <h2>Properties awaiting review</h2>
        <span>{{ properties.length }} results</span>
      </div>

      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Property</th>
              <th>Location</th>
              <th>Owner</th>
              <th>Rooms</th>
              <th>Images</th>
              <th>Submitted</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="property in properties"
              :key="property.id"
            >
              <td>
                <strong>{{ property.name || 'N/A' }}</strong>
                <small>Property ID: {{ property.id }}</small>
                <small class="description">
                  {{ property.description || 'No description' }}
                </small>
              </td>

              <td>
                <strong>{{ property.city || 'N/A' }}</strong>
                <small>{{ property.address || 'Address unavailable' }}</small>
                <small>
                  {{
                    [
                      property.district,
                      property.state,
                      property.pincode
                    ].filter(Boolean).join(', ')
                  }}
                </small>
              </td>

              <td>
                <strong>{{ property.owner?.name || 'N/A' }}</strong>
                <small>{{ property.owner?.email || 'N/A' }}</small>
                <small>{{ property.owner?.mobile || 'N/A' }}</small>
              </td>

              <td>{{ property.room_count ?? 0 }}</td>
              <td>{{ property.image_count ?? 0 }}</td>
              <td>{{ formatDate(property.created_at) }}</td>

              <td>
                <span class="pending-badge">
                  {{ property.verification_status || 'pending' }}
                </span>
              </td>

              <td>
                <button
                  class="view-btn"
                  @click="viewProperty(property.id)"
                >
                  Review Details →
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <p class="result-count">
        Showing {{ properties.length }} pending properties
      </p>
    </template>

  </div>
</template>

<style scoped>
.verification-page {
  min-height: calc(100vh - 70px);
  padding: 36px;
  background: #f7f7f5;
  color: #202020;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  margin-bottom: 28px;
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
  font-size: 32px;
}

.subtitle {
  margin-top: 8px;
  color: #737373;
}

.summary-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 22px;
  margin-bottom: 22px;
  background: white;
  border: 1px solid #e6e6e3;
  border-radius: 9px;
}

.summary-card span {
  color: #737373;
  font-size: 13px;
}

.summary-card strong {
  display: block;
  margin-top: 8px;
  font-size: 30px;
}

.pending-badge {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 20px;
  background: #fff1ce;
  color: #805b00;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
  white-space: nowrap;
}

.search-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 0 14px;
  margin-bottom: 26px;
  background: white;
  border: 1px solid #dededb;
  border-radius: 7px;
}

.search-icon {
  color: #777;
  font-size: 22px;
}

.search-bar input {
  flex: 1;
  min-width: 0;
  padding: 14px 0;
  border: none;
  outline: none;
  background: transparent;
  font-size: 14px;
}

.clear-btn {
  padding: 6px 10px;
  border: none;
  background: transparent;
  color: #555;
  cursor: pointer;
}

.secondary-btn,
.view-btn,
.state-box button {
  padding: 10px 14px;
  border: 1px solid #d5d5d2;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  font-weight: 600;
}

.secondary-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.list-heading {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  margin-bottom: 15px;
}

.list-heading h2 {
  margin: 0;
  font-size: 19px;
}

.list-heading span,
.result-count {
  color: #777;
  font-size: 13px;
}

.table-wrapper {
  overflow-x: auto;
  background: white;
  border: 1px solid #e6e6e3;
  border-radius: 9px;
}

table {
  width: 100%;
  min-width: 1150px;
  border-collapse: collapse;
  text-align: left;
}

th {
  padding: 15px;
  background: #fafaf9;
  color: #686868;
  font-size: 11px;
  text-transform: uppercase;
}

td {
  padding: 16px 15px;
  border-top: 1px solid #eeeeeb;
  font-size: 13px;
  vertical-align: top;
}

td strong,
td small {
  display: block;
  overflow-wrap: anywhere;
}

td strong {
  margin-bottom: 5px;
}

td small {
  margin-top: 4px;
  color: #777;
  line-height: 1.5;
}

.description {
  max-width: 220px;
}

.view-btn:hover,
.secondary-btn:hover {
  border-color: #777;
}

.state-box {
  padding: 45px 20px;
  text-align: center;
  background: white;
  border: 1px solid #e6e6e3;
  border-radius: 9px;
  color: #666;
}

.state-box h3 {
  color: #333;
}

.error {
  color: #a12727;
}

.result-count {
  margin-top: 16px;
}

@media (max-width: 700px) {
  .verification-page {
    padding: 22px 15px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  h1 {
    font-size: 27px;
  }

  .summary-card {
    align-items: flex-start;
  }

  .search-bar {
    padding: 0 10px;
  }
}
</style>
