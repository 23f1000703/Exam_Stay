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

const search = ref('')
const statusFilter = ref('')

const fetchBookings = async () => {

  loading.value = true
  error.value = ''

  try {

    const response = await fetch(
      `${API}/owner/bookings`,
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

const filteredBookings = computed(() => {

  let result = [...bookings.value]

  if (statusFilter.value) {

    result = result.filter(
      booking =>
        booking.status === statusFilter.value
    )

  }

  if (search.value.trim()) {

    const query =
      search.value.toLowerCase().trim()

    result = result.filter(booking => {

      return (
        String(booking.id)
          .toLowerCase()
          .includes(query) ||

        (booking.student_name || '')
          .toLowerCase()
          .includes(query) ||

        (booking.student_email || '')
          .toLowerCase()
          .includes(query) ||

        (booking.property_name || '')
          .toLowerCase()
          .includes(query)
      )

    })

  }

  return result
})

const confirmedBookings = computed(() =>
  bookings.value.filter(
    booking => booking.status === 'confirmed'
  ).length
)

const pendingBookings = computed(() =>
  bookings.value.filter(
    booking => booking.status === 'pending'
  ).length
)

const completedBookings = computed(() =>
  bookings.value.filter(
    booking => booking.status === 'completed'
  ).length
)

const formatDate = (date) => {

  if (!date) return '-'

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


<template>
  <div class="page">

    <div class="header">
      <div>
        <h1>All Bookings</h1>
        <p>View all bookings for your properties</p>
      </div>

      <button @click="router.push('/owner/dashboard')">
        ← Dashboard
      </button>
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div class="stats">

      <div class="stat-card">
        <span>Total Bookings</span>
        <strong>{{ bookings.length }}</strong>
      </div>

      <div class="stat-card">
        <span>Confirmed</span>
        <strong>{{ confirmedBookings }}</strong>
      </div>

      <div class="stat-card">
        <span>Pending</span>
        <strong>{{ pendingBookings }}</strong>
      </div>

      <div class="stat-card">
        <span>Completed</span>
        <strong>{{ completedBookings }}</strong>
      </div>

    </div>

    <section class="card">

      <div class="toolbar">

        <input
          v-model="search"
          type="text"
          placeholder="Search student, property or booking ID..."
        >

        <select v-model="statusFilter">
          <option value="">All Status</option>
          <option value="pending">Pending</option>
          <option value="confirmed">Confirmed</option>
          <option value="completed">Completed</option>
          <option value="cancelled">Cancelled</option>
        </select>

      </div>

      <div v-if="loading" class="loading">
        Loading bookings...
      </div>

      <div
        v-else-if="filteredBookings.length === 0"
        class="empty"
      >
        No bookings found.
      </div>

      <div v-else class="table-wrapper">

        <table>

          <thead>
            <tr>
              <th>Booking</th>
              <th>Student</th>
              <th>Property</th>
              <th>Room</th>
              <th>Stay</th>
              <th>Guests</th>
              <th>Amount</th>
              <th>Status</th>
              <th>Booked On</th>
            </tr>
          </thead>

          <tbody>

            <tr
              v-for="booking in filteredBookings"
              :key="booking.id"
            >

              <td>
                <strong>#{{ booking.id }}</strong>
              </td>

              <td>
                <div class="student">

                  <strong>
                    {{ booking.student_name || 'Unknown' }}
                  </strong>

                  <small>
                    {{ booking.student_email || '-' }}
                  </small>

                  <small>
                    {{ booking.student_mobile || '-' }}
                  </small>

                </div>
              </td>

              <td>
                {{ booking.property_name || '-' }}
              </td>

              <td>
                {{ booking.room_number || '-' }}
              </td>

              <td>
                <div class="dates">
                  <span>
                    {{ formatDate(booking.check_in) }}
                  </span>

                  <span>→</span>

                  <span>
                    {{ formatDate(booking.check_out) }}
                  </span>
                </div>
              </td>

              <td>
                {{ booking.number_of_guests }}
              </td>

              <td>
                <strong>
                  ₹{{ booking.total_amount }}
                </strong>
              </td>

              <td>

                <span
                  :class="[
                    'status',
                    booking.status
                  ]"
                >
                  {{ booking.status }}
                </span>

              </td>

              <td>
                {{ formatDate(booking.created_at) }}
              </td>

            </tr>

          </tbody>

        </table>

      </div>

    </section>

  </div>
</template>

<style scoped>
.page {
  max-width: 1400px;
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

.header button {
  padding: 10px 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 7px;
  cursor: pointer;
}

.stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 15px;
  margin-bottom: 20px;
}

.stat-card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0,0,0,.05);
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

.card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,.05);
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
  padding: 11px;
  border: 1px solid #ddd;
  border-radius: 7px;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  border-collapse: collapse;
  min-width: 1100px;
}

th {
  text-align: left;
  background: #f8f8f8;
  padding: 13px;
  font-size: 13px;
}

td {
  padding: 15px 13px;
  border-bottom: 1px solid #eee;
  font-size: 13px;
}

.student {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.student small {
  color: #777;
}

.dates {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.status {
  display: inline-block;
  padding: 5px 9px;
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

.status.completed {
  background: #e5eefc;
  color: #2457a6;
}

.status.cancelled {
  background: #ffe8e8;
  color: #c62828;
}

.loading,
.empty {
  padding: 50px;
  text-align: center;
  color: #777;
}

.error {
  padding: 14px;
  margin-bottom: 20px;
  border-radius: 8px;
  background: #ffe8e8;
  color: #b42318;
}

@media (max-width: 800px) {

  .page {
    padding: 15px;
  }

  .stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .toolbar {
    flex-direction: column;
  }

}
</style>