<template>
  <div class="page">

    <div class="header">
      <div>
        <h1>Upcoming Bookings</h1>
        <p>Review and manage your upcoming bookings</p>
      </div>

      <button class="back-btn" @click="router.push('/owner/dashboard')">
        ← Dashboard
      </button>
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div v-if="success" class="success">
      {{ success }}
    </div>

    <div class="stats">

      <div class="stat-card">
        <span>Total Upcoming</span>
        <strong>{{ bookings.length }}</strong>
      </div>

      <div class="stat-card">
        <span>Pending</span>
        <strong>{{ pendingCount }}</strong>
      </div>

      <div class="stat-card">
        <span>Confirmed</span>
        <strong>{{ confirmedCount }}</strong>
      </div>

    </div>

    <div class="toolbar">

      <input
        v-model="search"
        type="text"
        placeholder="Search booking, student, property..."
      >

      <select v-model="statusFilter">
        <option value="">All</option>
        <option value="pending">Pending</option>
        <option value="confirmed">Confirmed</option>
      </select>

    </div>

    <div v-if="loading" class="loading">
      Loading upcoming bookings...
    </div>

    <div
      v-else-if="filteredBookings.length === 0"
      class="empty"
    >
      No upcoming bookings found.
    </div>

    <div v-else class="booking-list">

      <div
        v-for="booking in filteredBookings"
        :key="booking.id"
        class="booking-card"
      >

        <div class="booking-top">

          <div>
            <h2>
              Booking #{{ booking.id }}
            </h2>

            <span
              :class="[
                'status',
                booking.status
              ]"
            >
              {{ booking.status }}
            </span>
          </div>

          <div class="amount">
            ₹{{ booking.total_amount }}
          </div>

        </div>

        <div class="details">

          <div class="detail">
            <label>Student</label>
            <p>{{ booking.customer_name || '-' }}</p>
          </div>

          <div class="detail">
            <label>Property</label>
            <p>{{ booking.property_name || '-' }}</p>
          </div>

          <div class="detail">
            <label>Room</label>
            <p>{{ booking.room_number || '-' }}</p>
          </div>

          <div class="detail">
            <label>Guests</label>
            <p>{{ booking.number_of_guests }}</p>
          </div>

          <div class="detail">
            <label>Check-in</label>
            <p>{{ formatDate(booking.check_in) }}</p>
          </div>

          <div class="detail">
            <label>Check-out</label>
            <p>{{ formatDate(booking.check_out) }}</p>
          </div>

          <div class="detail">
            <label>Booked On</label>
            <p>{{ formatDate(booking.created_at) }}</p>
          </div>

        </div>

        <div
          v-if="booking.status === 'pending'"
          class="booking-actions"
        >

          <button
            class="confirm-btn"
            :disabled="processingId === booking.id"
            @click="updateBooking(booking.id, 'confirmed')"
          >
            {{
              processingId === booking.id
                ? 'Processing...'
                : '✓ Confirm Booking'
            }}
          </button>

          <button
            class="reject-btn"
            :disabled="processingId === booking.id"
            @click="updateBooking(booking.id, 'cancelled')"
          >
            ✕ Reject Booking
          </button>

        </div>

        <div
          v-else
          class="confirmed-message"
        >
          ✓ This booking is confirmed.
        </div>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const API = 'http://127.0.0.1:5000/api'

const bookings = ref([])
const loading = ref(true)
const error = ref('')
const success = ref('')

const search = ref('')
const statusFilter = ref('')
const processingId = ref(null)

const fetchBookings = async () => {

  loading.value = true
  error.value = ''

  try {

    const response = await fetch(
      `${API}/owner/upcoming-bookings`,
      {
        method: 'GET',
        headers: {
          'Authentication-Token': authStore.token
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      error.value =
        data.message || 'Failed to load bookings.'
      return
    }

    bookings.value = data.bookings || []

  } catch (err) {

    console.error(err)

    error.value =
      'Unable to connect to server.'

  } finally {

    loading.value = false

  }
}

const updateBooking = async (
  bookingId,
  status
) => {

  const action =
    status === 'confirmed'
      ? 'confirm'
      : 'reject'

  const confirmed = window.confirm(
    `Are you sure you want to ${action} this booking?`
  )

  if (!confirmed) {
    return
  }

  processingId.value = bookingId
  error.value = ''
  success.value = ''

  try {

    const response = await fetch(
      `${API}/owner/upcoming-bookings/${bookingId}`,
      {
        method: 'PUT',
        headers: {
          'Authentication-Token': authStore.token,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          status
        })
      }
    )

    const data = await response.json()

    if (!response.ok) {
      error.value =
        data.message || 'Failed to update booking.'
      return
    }

    const booking = bookings.value.find(
      item => item.id === bookingId
    )

    if (booking) {

      if (status === 'cancelled') {
        bookings.value =
          bookings.value.filter(
            item => item.id !== bookingId
          )
      } else {
        booking.status = status
      }

    }

    success.value =
      data.message ||
      'Booking updated successfully.'

  } catch (err) {

    console.error(err)

    error.value =
      'Unable to connect to server.'

  } finally {

    processingId.value = null

  }
}

const filteredBookings = computed(() => {

  let result = [...bookings.value]

  if (statusFilter.value) {

    result = result.filter(
      booking =>
        booking.status === statusFilter.value
    )

  }

  const query =
    search.value.trim().toLowerCase()

  if (query) {

    result = result.filter(booking => {

      return (
        String(booking.id)
          .includes(query) ||

        (booking.customer_name || '')
          .toLowerCase()
          .includes(query) ||

        (booking.property_name || '')
          .toLowerCase()
          .includes(query) ||

        (booking.room_number || '')
          .toLowerCase()
          .includes(query)
      )

    })

  }

  return result
})

const pendingCount = computed(() =>
  bookings.value.filter(
    booking => booking.status === 'pending'
  ).length
)

const confirmedCount = computed(() =>
  bookings.value.filter(
    booking => booking.status === 'confirmed'
  ).length
)

const formatDate = (date) => {

  if (!date) {
    return '-'
  }

  return new Date(date).toLocaleDateString(
    'en-IN',
    {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    }
  )
}

onMounted(() => {
  fetchBookings()
})
</script>

<style scoped>
.page {
  max-width: 1100px;
  margin: 0 auto;
  padding: 30px;
  min-height: 100vh;
  background: #f6f7fb;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.header h1 {
  margin: 0;
  font-size: 30px;
}

.header p {
  margin: 6px 0 0;
  color: #777;
}

.back-btn {
  padding: 10px 16px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 7px;
  cursor: pointer;
}

.stats {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, .05);
}

.stat-card span {
  display: block;
  color: #777;
  font-size: 13px;
  margin-bottom: 8px;
}

.stat-card strong {
  font-size: 25px;
}

.toolbar {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.toolbar input {
  flex: 1;
}

.toolbar input,
.toolbar select {
  padding: 11px 13px;
  border: 1px solid #ddd;
  border-radius: 7px;
  background: white;
}

.booking-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.booking-card {
  background: white;
  border-radius: 12px;
  padding: 22px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, .05);
}

.booking-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: 18px;
  border-bottom: 1px solid #eee;
}

.booking-top h2 {
  display: inline-block;
  margin: 0 12px 0 0;
  font-size: 19px;
}

.amount {
  font-size: 20px;
  font-weight: 700;
}

.status {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
  text-transform: capitalize;
}

.status.pending {
  background: #fff3cd;
  color: #856404;
}

.status.confirmed {
  background: #e5f8eb;
  color: #18853b;
}

.details {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  padding: 20px 0;
}

.detail label {
  display: block;
  color: #888;
  font-size: 12px;
  margin-bottom: 5px;
}

.detail p {
  margin: 0;
  font-weight: 500;
}

.booking-actions {
  display: flex;
  gap: 10px;
  padding-top: 18px;
  border-top: 1px solid #eee;
}

.confirm-btn,
.reject-btn {
  padding: 11px 18px;
  border-radius: 7px;
  cursor: pointer;
  font-weight: 600;
}

.confirm-btn {
  background: #18853b;
  color: white;
}

.reject-btn {
  background: #c62828;
  color: white;
}

.confirm-btn:disabled,
.reject-btn:disabled {
  opacity: .6;
  cursor: not-allowed;
}

.confirmed-message {
  padding-top: 15px;
  color: #18853b;
  font-weight: 600;
}

.loading,
.empty {
  background: white;
  padding: 50px;
  text-align: center;
  border-radius: 12px;
  color: #777;
}

.error {
  padding: 13px;
  background: #ffe8e8;
  color: #b42318;
  border-radius: 8px;
  margin-bottom: 20px;
}

.success {
  padding: 13px;
  background: #e8f8ed;
  color: #18753b;
  border-radius: 8px;
  margin-bottom: 20px;
}

@media (max-width: 800px) {

  .page {
    padding: 15px;
  }

  .stats {
    grid-template-columns: 1fr;
  }

  .toolbar {
    flex-direction: column;
  }

  .details {
    grid-template-columns: repeat(2, 1fr);
  }

  .booking-top {
    align-items: flex-start;
    gap: 15px;
  }

  .booking-actions {
    flex-direction: column;
  }

  .confirm-btn,
  .reject-btn {
    width: 100%;
  }
}
</style>