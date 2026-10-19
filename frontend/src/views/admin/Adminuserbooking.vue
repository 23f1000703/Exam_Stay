
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const bookings = ref([])
const totalBookings = ref(0)
const search = ref('')
const status = ref('')
const loading = ref(false)
const error = ref('')

let searchTimer = null

const fetchBookings = async () => {
  try {
    loading.value = true
    error.value = ''

    const params = new URLSearchParams()

    if (search.value.trim()) {
      params.set('search', search.value.trim())
    }

    if (status.value) {
      params.set('status', status.value)
    }

    const response = await fetch(
      `http://localhost:5000/api/admin/bookings?${params.toString()}`,
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
        `Invalid server response. HTTP ${response.status}. Check authentication or API route.`
      )
    }

    if (!response.ok) {
      throw new Error(data.message || 'Failed to fetch bookings')
    }

    bookings.value = data.bookings || []
    totalBookings.value = data.total_bookings || 0

  } catch (err) {
    console.error('Bookings API error:', err)
    error.value = err.message || 'Unable to fetch bookings'
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  clearTimeout(searchTimer)
  searchTimer = setTimeout(fetchBookings, 400)
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

const formatDateTime = (value) => {
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

const formatAmount = (value) => {
  if (value === null || value === undefined) return 'N/A'

  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 2
  }).format(value)
}

const statusClass = (value) => {
  const normalized = (value || 'unknown')
    .toLowerCase()
    .replaceAll(' ', '-')

  if (
    ['pending', 'confirmed', 'cancelled', 'completed',
      'paid', 'failed', 'refunded', 'unpaid'].includes(normalized)
  ) {
    return normalized
  }

  return 'other'
}

onMounted(fetchBookings)

onUnmounted(() => {
  clearTimeout(searchTimer)
})
</script>

<template>
  <div class="bookings-page">

    <header class="page-header">
      <div>
        <p class="eyebrow">EXAMSTAY ADMIN</p>
        <h1>Bookings Management</h1>
        <p class="subtitle">
          View which student booked which property, along with
          stay details and payment information.
        </p>
      </div>

      <button
        class="refresh-btn"
        :disabled="loading"
        @click="fetchBookings"
      >
        ↻ Refresh
      </button>
    </header>

    <section class="summary-card">
      <span>Total matching bookings</span>
      <strong>{{ totalBookings }}</strong>
    </section>

    <section class="toolbar">
      <input
        v-model="search"
        type="text"
        placeholder="Search student name, property name, email, room..."
        @input="handleSearch"
      />

      <select v-model="status" @change="fetchBookings">
        <option value="">All booking statuses</option>
        <option value="pending">Pending</option>
        <option value="confirmed">Confirmed</option>
        <option value="cancelled">Cancelled</option>
        <option value="completed">Completed</option>
      </select>
    </section>

    <div v-if="loading" class="state-box">
      Loading bookings...
    </div>

    <div v-else-if="error" class="state-box error">
      <p>{{ error }}</p>
      <button class="refresh-btn" @click="fetchBookings">
        Try Again
      </button>
    </div>

    <div v-else-if="bookings.length === 0" class="state-box">
      No bookings found. Try another student or property name.
    </div>

    <template v-else>
      <div class="table-wrapper">
        <table>
          <thead>
            <tr>
              <th>Booking</th>
              <th>Student</th>
              <th>Property</th>
              <th>Room</th>
              <th>Stay Details</th>
              <th>Amount</th>
              <th>Booking Status</th>
              <th>Payment Details</th>
            </tr>
          </thead>

          <tbody>
            <tr
              v-for="booking in bookings"
              :key="booking.id"
            >
              <!-- Booking -->
              <td>
                <strong>#{{ booking.id }}</strong>
                <small>Booked on</small>
                <small>{{ formatDateTime(booking.created_at) }}</small>
              </td>

              <!-- Student -->
              <td>
                <strong>
                  {{ booking.student?.name || 'N/A' }}
                </strong>
                <small>
                  ID: {{ booking.student?.id ?? 'N/A' }}
                </small>
                <small>
                  {{ booking.student?.email || 'N/A' }}
                </small>
                <small>
                  Mobile: {{ booking.student?.mobile || 'N/A' }}
                </small>
                <small>
                  {{ booking.student?.college_name || 'N/A' }}
                </small>
                <small>
                  {{ booking.student?.course || '' }}
                </small>
              </td>

              <!-- Property -->
              <td>
                <strong>
                  {{ booking.property?.name || 'N/A' }}
                </strong>
                <small>
                  Property ID: {{ booking.property?.id ?? 'N/A' }}
                </small>
                <small>
                  {{ booking.property?.address || '' }}
                </small>
                <small>
                  {{
                    [
                      booking.property?.city,
                      booking.property?.district,
                      booking.property?.state
                    ].filter(Boolean).join(', ')
                  }}
                </small>
                <small>
                  {{ booking.property?.pincode || '' }}
                </small>
              </td>

              <!-- Room -->
              <td>
                <strong>
                  {{ booking.room?.room_number || 'N/A' }}
                </strong>
                <small>
                  Room ID: {{ booking.room?.id ?? 'N/A' }}
                </small>
                <small>
                  {{ booking.room?.room_type || 'N/A' }}
                </small>
                <small>
                  Capacity: {{ booking.room?.capacity ?? 'N/A' }}
                </small>
                <small>
                  Per night:
                  {{ formatAmount(booking.room?.price_per_night) }}
                </small>
              </td>

              <!-- Dates and guests -->
              <td>
                <small>Check-in</small>
                <strong>{{ formatDate(booking.check_in) }}</strong>
                <small>Check-out</small>
                <strong>{{ formatDate(booking.check_out) }}</strong>
                <small>
                  Guests: {{ booking.number_of_guests ?? 'N/A' }}
                </small>
              </td>

              <!-- Amount -->
              <td>
                <strong>{{ formatAmount(booking.total_amount) }}</strong>
              </td>

              <!-- Booking status -->
              <td>
                <span
                  class="status"
                  :class="statusClass(booking.status)"
                >
                  {{ booking.status || 'Unknown' }}
                </span>
              </td>

              <!-- Payment -->
              <td>
                <strong>
                  {{ booking.payment?.status || 'Unpaid' }}
                </strong>
                <small>
                  Amount:
                  {{ formatAmount(booking.payment?.amount) }}
                </small>
                <small>
                  Method:
                  {{ booking.payment?.payment_method || 'N/A' }}
                </small>
                <small>
                  Transaction:
                  {{ booking.payment?.transaction_id || 'N/A' }}
                </small>
                <small>
                  Paid on:
                  {{ formatDateTime(booking.payment?.paid_at) }}
                </small>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <p class="result-count">
        Showing {{ bookings.length }} matching bookings
      </p>
    </template>

  </div>
</template>

<style scoped>
.bookings-page {
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
  max-width: 650px;
  color: #737373;
  line-height: 1.6;
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

.refresh-btn {
  padding: 11px 15px;
  border: 1px solid #d5d5d2;
  border-radius: 6px;
  background: white;
  cursor: pointer;
  font-weight: 600;
  white-space: nowrap;
}

.refresh-btn:disabled {
  cursor: not-allowed;
  opacity: 0.6;
}

.table-wrapper {
  overflow-x: auto;
  background: white;
  border: 1px solid #e6e6e3;
  border-radius: 9px;
}

table {
  width: 100%;
  min-width: 1600px;
  border-collapse: collapse;
  text-align: left;
}

th {
  padding: 15px;
  background: #fafaf9;
  color: #686868;
  font-size: 11px;
  text-transform: uppercase;
  white-space: nowrap;
}

td {
  max-width: 260px;
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
  margin-bottom: 6px;
}

td small {
  margin-top: 5px;
  color: #777;
  line-height: 1.5;
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

.status.pending,
.status.unpaid {
  background: #fff1ce;
  color: #805b00;
}

.status.confirmed,
.status.completed,
.status.paid {
  background: #e1f5e7;
  color: #176b35;
}

.status.cancelled,
.status.failed,
.status.rejected {
  background: #fbe5e5;
  color: #a12727;
}

.status.refunded {
  background: #e8eaff;
  color: #383f94;
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
  .bookings-page {
    padding: 22px 15px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  h1 {
    font-size: 27px;
  }

  .toolbar {
    flex-direction: column;
  }
}
</style>
