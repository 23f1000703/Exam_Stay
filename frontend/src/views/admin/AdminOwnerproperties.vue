
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const properties = ref([])
const search = ref('')
const status = ref('')
const loading = ref(false)
const error = ref('')
const totalProperties = ref(0)

let searchTimer = null

const fetchProperties = async () => {
  try {
    loading.value = true
    error.value = ''

    const params = new URLSearchParams()

    params.set('search', search.value.trim())

    if (status.value) {
      params.set('status', status.value)
    }

    const response = await fetch(
      `http://localhost:5000/api/admin/properties?${params.toString()}`,
      {
        method: 'GET',
        headers: {
          'Authentication-Token': authStore.token
        }
      }
    )
    console.log('Token exists:', Boolean(authStore.token))

    const text = await response.text()
    console.log('API URL:', `http://localhost:5000/api/admin/properties?${params.toString()}`)
    console.log('HTTP STATUS:', response.status)
    console.log('RESPONSE:', text)

    
    let data

    try {
      data = JSON.parse(text)
    } catch {
      throw new Error(
        `Invalid server response. HTTP ${response.status}`
      )
    }

    if (!response.ok) {
      throw new Error(data.message || 'Failed to fetch properties')
    }

    properties.value = data.properties || []
    totalProperties.value = data.total_properties || 0

  } catch (err) {
    console.error(err)
    error.value = err.message || 'Unable to fetch properties'
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(fetchProperties, 400)
}

const viewProperty = (propertyId) => {
  router.push(`/admin/properties/${propertyId}`)
}

const formatDate = (date) => {
  if (!date) return 'N/A'

  return new Date(date).toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

const statusClass = (value) => {
  const normalized = (value || 'pending').toLowerCase()

  if (['pending', 'verified', 'rejected'].includes(normalized)) {
    return normalized
  }

  return 'other'
}

onMounted(fetchProperties)

onUnmounted(() => {
  clearTimeout(searchTimer)
})
</script>

<template>
  <div class="properties-page">

    <header class="page-header">
      <div>
        <p class="eyebrow">EXAMSTAY ADMIN</p>
        <h1>Properties</h1>
        <p class="subtitle">
          Manage registered properties and review their details.
        </p>
      </div>

      <button
        class="refresh-btn"
        @click="fetchProperties"
        :disabled="loading"
      >
        Refresh
      </button>
    </header>

    <div class="summary-card">
      <span>Total matching properties</span>
      <strong>{{ totalProperties }}</strong>
    </div>

    <div class="toolbar">
      <input
        v-model="search"
        @input="handleSearch"
        type="text"
        placeholder="Search property, city, address or owner..."
      />

      <select v-model="status" @change="fetchProperties">
        <option value="">All statuses</option>
        <option value="pending">Pending</option>
        <option value="verified">Verified</option>
        <option value="rejected">Rejected</option>
      </select>
    </div>

    <div v-if="loading" class="state-box">
      Loading properties...
    </div>

    <div v-else-if="error" class="state-box error">
      <p>{{ error }}</p>
      <button @click="fetchProperties">Try Again</button>
    </div>

    <div v-else-if="properties.length === 0" class="state-box">
      No properties found.
    </div>

    <div v-else class="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Property</th>
            <th>Location</th>
            <th>Owner</th>
            <th>Rooms</th>
            <th>Images</th>
            <th>Verification</th>
            <th>Created</th>
            <th>Action</th>
          </tr>
        </thead>

        <tbody>
          <tr
            v-for="property in properties"
            :key="property.id"
          >
            <td>
              <strong>{{ property.name }}</strong>
              <small>Property ID: {{ property.id }}</small>
            </td>

            <td>
              <strong>{{ property.city || 'N/A' }}</strong>
              <small>
                {{ property.address || 'Address unavailable' }}
              </small>
              <small>
                {{ property.district || '' }}
                {{ property.state ? ', ' + property.state : '' }}
                {{ property.pincode ? ' - ' + property.pincode : '' }}
              </small>
            </td>

            <td>
              <strong>{{ property.owner?.name || 'N/A' }}</strong>
              <small>{{ property.owner?.email || 'N/A' }}</small>
              <small>{{ property.owner?.mobile || 'N/A' }}</small>
            </td>

            <td>{{ property.room_count ?? 0 }}</td>

            <td>{{ property.image_count ?? 0 }}</td>

            <td>
              <span
                class="status"
                :class="statusClass(property.verification_status)"
              >
                {{ property.verification_status || 'Pending' }}
              </span>
            </td>

            <td>{{ formatDate(property.created_at) }}</td>

            <td>
              <button
                class="view-btn"
                @click="viewProperty(property.id)"
              >
                View Details →
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <p v-if="!loading && !error && properties.length" class="result-count">
      Showing {{ properties.length }} matching properties
    </p>

  </div>
</template>

<style scoped>
.properties-page {
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
  font-size: 34px;
}

.subtitle {
  color: #737373;
  margin-top: 8px;
}

.summary-card {
  padding: 20px;
  margin-bottom: 22px;
  background: white;
  border: 1px solid #e6e6e3;
  border-radius: 9px;
}

.summary-card span {
  display: block;
  color: #737373;
  font-size: 13px;
}

.summary-card strong {
  display: block;
  margin-top: 8px;
  font-size: 28px;
}

.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.toolbar input,
.toolbar select {
  padding: 12px 14px;
  border: 1px solid #dededb;
  border-radius: 6px;
  background: white;
  font-size: 14px;
}

.toolbar input {
  flex: 1;
  min-width: 0;
}

.refresh-btn,
.view-btn,
.state-box button {
  padding: 10px 14px;
  border: 1px solid #d5d5d2;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  font-weight: 600;
}

.table-wrapper {
  overflow-x: auto;
  background: white;
  border: 1px solid #e6e6e3;
  border-radius: 9px;
}

table {
  width: 100%;
  min-width: 1100px;
  border-collapse: collapse;
  text-align: left;
}

th {
  padding: 15px;
  background: #fafaf9;
  color: #686868;
  font-size: 12px;
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
}

.status {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 20px;
  background: #eee;
  color: #555;
  font-size: 12px;
  text-transform: capitalize;
}

.status.pending {
  background: #fff1ce;
  color: #805b00;
}

.status.verified {
  background: #e1f5e7;
  color: #176b35;
}

.status.rejected {
  background: #fbe5e5;
  color: #a12727;
}

.view-btn:hover,
.refresh-btn:hover {
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

.error {
  color: #a12727;
}

.result-count {
  margin-top: 16px;
  color: #777;
  font-size: 13px;
}

@media (max-width: 700px) {
  .properties-page {
    padding: 22px 15px;
  }

  .page-header {
    align-items: flex-start;
  }

  h1 {
    font-size: 28px;
  }

  .toolbar {
    flex-direction: column;
  }
}
</style>
