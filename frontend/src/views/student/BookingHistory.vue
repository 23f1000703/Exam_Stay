<template>
  <div class="history-page">
    <header class="page-header">
      <div>
        <h1>My Booking History</h1>
        <p>View all your previous and current stays.</p>
      </div>

      <RouterLink to="/student" class="back-btn">
        Dashboard
      </RouterLink>
    </header>

    <div class="summary">
      <div class="summary-card">
        <span>Total Bookings</span>
        <strong>{{ bookings.length }}</strong>
      </div>
      <div class="summary-card">
        <span>Confirmed</span>
        <strong>{{ countStatus('confirmed') }}</strong>
      </div>
      <div class="summary-card">
        <span>Completed</span>
        <strong>{{ countStatus('completed') }}</strong>
      </div>
      <div class="summary-card">
        <span>Cancelled</span>
        <strong>{{ countStatus('cancelled') }}</strong>
      </div>
    </div>

    <div class="filters">
      <input
        v-model="search"
        type="text"
        placeholder="Search hotel or city..."
      />

      <select v-model="selectedStatus">
        <option value="">All statuses</option>
        <option value="pending">Pending</option>
        <option value="confirmed">Confirmed</option>
        <option value="completed">Completed</option>
        <option value="cancelled">Cancelled</option>
        <option value="rejected">Rejected</option>
      </select>
    </div>

    <div v-if="loading" class="empty-state">
      Loading booking history...
    </div>

    <div v-else-if="errorMessage" class="error">
      {{ errorMessage }}
      <button @click="fetchHistory">Try Again</button>
    </div>

    <div
      v-else-if="filteredBookings.length === 0"
      class="empty-state"
    >
      <h3>No bookings found</h3>
      <p>Your bookings will appear here after you book a stay.</p>
      <RouterLink to="/student/search" class="primary-btn">
        Find a Stay
      </RouterLink>
    </div>

    <div v-else class="booking-list">
      <article
        v-for="booking in filteredBookings"
        :key="booking.id"
        class="booking-card"
      >
        <div class="booking-top">
          <div>
            <span class="booking-id">
              Booking #{{ booking.id }}
            </span>
            <h2>{{ booking.property.name }}</h2>
            <p class="location">
              📍 {{ booking.property.city || 'Location unavailable' }}
            </p>
          </div>

          <span
            class="status"
            :class="statusClass(booking.status)"
          >
            {{ booking.status || 'Unknown' }}
          </span>
        </div>

        <div class="details-grid">
          <div>
            <span>Check-in</span>
            <strong>{{ formatDate(booking.check_in) }}</strong>
          </div>
          <div>
            <span>Check-out</span>
            <strong>{{ formatDate(booking.check_out) }}</strong>
          </div>
          <div>
            <span>Room</span>
            <strong>
              {{ booking.room.room_number || 'Not specified' }}
            </strong>
          </div>
          <div>
            <span>Guests</span>
            <strong>{{ booking.number_of_guests ?? '—' }}</strong>
          </div>
        </div>

        <div class="booking-footer">
          <div>
            <span class="amount-label">Total amount</span>
            <strong class="amount">
              {{ formatPrice(booking.total_amount) }}
            </strong>
          </div>

          <span class="booked-date">
            Booked on {{ formatDate(booking.created_at) }}
          </span>
        </div>
      </article>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const bookings = ref([])
const loading = ref(false)
const errorMessage = ref('')
const search = ref('')
const selectedStatus = ref('')

const fetchHistory = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await fetch(
      'http://localhost:5000/api/student/booking-history',
      {
        headers: {
          'Authentication-Token': authStore.token
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(
        data.message || 'Unable to fetch booking history.'
      )
    }

    bookings.value = data.bookings || []
  } catch (error) {
    console.error('Booking history error:', error)
    errorMessage.value = error.message || 'Something went wrong.'
  } finally {
    loading.value = false
  }
}

const filteredBookings = computed(() => {
  return bookings.value.filter((booking) => {
    const query = search.value.trim().toLowerCase()

    const matchesSearch =
      !query ||
      (booking.property?.name || '').toLowerCase().includes(query) ||
      (booking.property?.city || '').toLowerCase().includes(query)

    const matchesStatus =
      !selectedStatus.value ||
      (booking.status || '').toLowerCase() ===
        selectedStatus.value.toLowerCase()

    return matchesSearch && matchesStatus
  })
})

const countStatus = (status) => {
  return bookings.value.filter(
    (booking) =>
      (booking.status || '').toLowerCase() === status
  ).length
}

const statusClass = (status) => {
  const value = (status || '').toLowerCase()

  if (value === 'confirmed') return 'confirmed'
  if (value === 'completed') return 'completed'
  if (value === 'cancelled') return 'cancelled'
  if (value === 'rejected') return 'rejected'

  return 'pending'
}

const formatDate = (value) => {
  if (!value) return '—'

  const date = new Date(value)

  if (Number.isNaN(date.getTime())) return '—'

  return date.toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

const formatPrice = (amount) => {
  if (amount == null) return 'Not available'

  return Number(amount).toLocaleString('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 2
  })
}

onMounted(fetchHistory)
</script>

<style scoped>
.history-page {
  min-height: 100vh;
  padding: 32px;
  background: #f5f7fb;
  color: #1e293b;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  margin-bottom: 26px;
}

.page-header h1 {
  margin: 0 0 8px;
  font-size: 28px;
}

.page-header p {
  margin: 0;
  color: #64748b;
}

.back-btn {
  text-decoration: none;
  padding: 10px 16px;
  border: 1px solid #dbe2ea;
  border-radius: 8px;
  background: white;
  color: #334155;
}

.summary {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.summary-card {
  padding: 20px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 12px;
}

.summary-card span,
.details-grid span,
.amount-label {
  display: block;
  color: #64748b;
  font-size: 13px;
  margin-bottom: 8px;
}

.summary-card strong {
  font-size: 26px;
}

.filters {
  display: flex;
  gap: 12px;
  margin-bottom: 22px;
}

.filters input,
.filters select {
  padding: 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: white;
  font: inherit;
}

.filters input {
  flex: 1;
  min-width: 0;
}

.booking-list {
  display: grid;
  gap: 18px;
}

.booking-card {
  padding: 22px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
}

.booking-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 12px;
  padding-bottom: 18px;
  border-bottom: 1px solid #e2e8f0;
}

.booking-id {
  color: #64748b;
  font-size: 12px;
}

.booking-top h2 {
  margin: 8px 0;
  font-size: 20px;
}

.location {
  margin: 0;
  color: #64748b;
  font-size: 14px;
}

.status {
  padding: 7px 11px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
  text-transform: capitalize;
  white-space: nowrap;
}

.confirmed {
  background: #dcfce7;
  color: #166534;
}

.completed {
  background: #dbeafe;
  color: #1d4ed8;
}

.cancelled,
.rejected {
  background: #fee2e2;
  color: #991b1b;
}

.pending {
  background: #fef3c7;
  color: #92400e;
}

.details-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 18px;
  padding: 20px 0;
}

.details-grid strong {
  font-size: 14px;
  overflow-wrap: anywhere;
}

.booking-footer {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.amount {
  font-size: 20px;
}

.booked-date {
  color: #64748b;
  font-size: 13px;
}

.empty-state {
  padding: 48px 20px;
  text-align: center;
  background: white;
  border-radius: 12px;
  color: #64748b;
}

.empty-state h3 {
  color: #334155;
}

.primary-btn {
  display: inline-block;
  margin-top: 12px;
  padding: 11px 16px;
  background: #2563eb;
  color: white;
  border-radius: 8px;
  text-decoration: none;
}

.error {
  padding: 16px;
  color: #991b1b;
  background: #fee2e2;
  border-radius: 8px;
  overflow-wrap: anywhere;
}

@media (max-width: 800px) {
  .summary {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .details-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 550px) {
  .history-page {
    padding: 16px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .filters {
    flex-direction: column;
  }

  .booking-top,
  .booking-footer {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>