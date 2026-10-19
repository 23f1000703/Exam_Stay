<template>
  <div class="page">

    <div class="header">
      <div>
        <h1>Student Details</h1>
        <p>Student profile and complete booking history</p>
      </div>

      <button class="back-btn" @click="router.back()">
        ← Back
      </button>
    </div>

    <div v-if="loading" class="loading">
      Loading student details...
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else-if="student">

      <!-- Student Information -->
      <div class="card student-card">

        <div class="profile">
          <img
            v-if="student.profile_photo"
            :src="getImageUrl(student.profile_photo)"
            alt="Profile"
          />

          <div v-else class="profile-placeholder">
            {{ student.name?.charAt(0).toUpperCase() }}
          </div>
        </div>

        <div class="student-info">
          <h2>{{ student.name }}</h2>

          <div class="info-grid">
            <div>
              <span>Email</span>
              <strong>{{ student.email || 'N/A' }}</strong>
            </div>

            <div>
              <span>Mobile</span>
              <strong>{{ student.mobile || 'N/A' }}</strong>
            </div>

            <div>
              <span>College</span>
              <strong>{{ student.college_name || 'N/A' }}</strong>
            </div>

            <div>
              <span>Course</span>
              <strong>{{ student.course || 'N/A' }}</strong>
            </div>

            <div>
              <span>Student ID</span>
              <strong>{{ student.student_id || 'N/A' }}</strong>
            </div>
          </div>
        </div>

      </div>

      <!-- Booking Summary -->
      <div class="section">
        <h2>Booking Summary</h2>

        <div class="summary-grid">

          <div class="summary-card">
            <span>Total Bookings</span>
            <strong>{{ bookingSummary.total_bookings }}</strong>
          </div>

          <div class="summary-card">
            <span>Confirmed</span>
            <strong>{{ bookingSummary.confirmed }}</strong>
          </div>

          <div class="summary-card">
            <span>Pending</span>
            <strong>{{ bookingSummary.pending }}</strong>
          </div>

          <div class="summary-card">
            <span>Cancelled</span>
            <strong>{{ bookingSummary.cancelled }}</strong>
          </div>

          <div class="summary-card">
            <span>Completed</span>
            <strong>{{ bookingSummary.completed }}</strong>
          </div>

        </div>
      </div>

      <!-- Booking History -->
      <div class="section">

        <div class="section-header">
          <div>
            <h2>Booking History</h2>
            <p>All bookings made by this student</p>
          </div>

          <span class="booking-count">
            {{ bookings.length }} bookings
          </span>
        </div>

        <div v-if="bookings.length === 0" class="empty">
          This student has not made any booking yet.
        </div>

        <div v-else class="booking-list">

          <div
            v-for="booking in bookings"
            :key="booking.booking_id"
            class="booking-card"
          >

            <div class="booking-header">

              <div>
                <h3>{{ booking.property.name }}</h3>

                <p>
                  {{ booking.property.address }},
                  {{ booking.property.city }},
                  {{ booking.property.state }}
                </p>
              </div>

              <span
                class="status"
                :class="booking.booking_status"
              >
                {{ booking.booking_status }}
              </span>

            </div>

            <div class="booking-details">

              <div>
                <span>Booking ID</span>
                <strong>#{{ booking.booking_id }}</strong>
              </div>

              <div>
                <span>Room</span>
                <strong>
                  {{ booking.room.room_number || 'N/A' }}
                </strong>
              </div>

              <div>
                <span>Room Type</span>
                <strong>
                  {{ booking.room.room_type || 'N/A' }}
                </strong>
              </div>

              <div>
                <span>Guests</span>
                <strong>
                  {{ booking.number_of_guests }}
                </strong>
              </div>

              <div>
                <span>Check-in</span>
                <strong>
                  {{ formatDate(booking.check_in) }}
                </strong>
              </div>

              <div>
                <span>Check-out</span>
                <strong>
                  {{ formatDate(booking.check_out) }}
                </strong>
              </div>

              <div>
                <span>Total Amount</span>
                <strong>
                  ₹{{ booking.total_amount }}
                </strong>
              </div>

              <div>
                <span>Booked At</span>
                <strong>
                  {{ formatDate(booking.booked_at) }}
                </strong>
              </div>

            </div>

            <!-- Payment -->
            <div class="payment">

              <h4>Payment</h4>

              <div class="payment-grid">

                <div>
                  <span>Status</span>
                  <strong>
                    {{ booking.payment.status || 'N/A' }}
                  </strong>
                </div>

                <div>
                  <span>Amount</span>
                  <strong>
                    ₹{{ booking.payment.amount || 0 }}
                  </strong>
                </div>

                <div>
                  <span>Method</span>
                  <strong>
                    {{ booking.payment.method || 'N/A' }}
                  </strong>
                </div>

                <div>
                  <span>Transaction ID</span>
                  <strong>
                    {{ booking.payment.transaction_id || 'N/A' }}
                  </strong>
                </div>

                <div>
                  <span>Paid At</span>
                  <strong>
                    {{ formatDate(booking.payment.paid_at) }}
                  </strong>
                </div>

              </div>

            </div>

          </div>

        </div>

      </div>

    </div>

  </div>
</template>

<script setup>

import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const student = ref(null)
const bookings = ref([])
const bookingSummary = ref({
  total_bookings: 0,
  confirmed: 0,
  pending: 0,
  cancelled: 0,
  completed: 0
})

const loading = ref(true)
const error = ref('')

const fetchStudent = async () => {

  try {

    const studentId = route.params.student_id

    const response = await fetch(
      `http://localhost:5000/api/admin/students/${studentId}`,
      {
        headers: {
          'Authentication-Token': authStore.token
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(
        data.message || 'Failed to fetch student details.'
      )
    }

    student.value = data.student
    bookings.value = data.bookings || []

    bookingSummary.value = data.booking_summary || {
      total_bookings: 0,
      confirmed: 0,
      pending: 0,
      cancelled: 0,
      completed: 0
    }

  } catch (err) {

    error.value = err.message

  } finally {

    loading.value = false

  }
}

const formatDate = (date) => {

  if (!date) {
    return 'N/A'
  }

  return new Date(date).toLocaleString('en-IN', {
    dateStyle: 'medium',
    timeStyle: 'short'
  })
}

const getImageUrl = (path) => {

  if (!path) {
    return ''
  }

  if (path.startsWith('http')) {
    return path
  }

  return `http://localhost:5000/${path}`
}

onMounted(() => {
  fetchStudent()
})

</script>

<style scoped>

.page {
  padding: 30px;
  background: #f7f8fa;
  min-height: 100vh;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
}

.header h1 {
  margin: 0;
  font-size: 28px;
}

.header p {
  margin-top: 6px;
  color: #777;
}

.back-btn {
  border: none;
  background: #222;
  color: white;
  padding: 10px 18px;
  border-radius: 7px;
  cursor: pointer;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.student-card {
  display: flex;
  gap: 25px;
  align-items: center;
}

.profile img,
.profile-placeholder {
  width: 100px;
  height: 100px;
  border-radius: 50%;
}

.profile img {
  object-fit: cover;
}

.profile-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: #e9ecef;
  font-size: 35px;
  font-weight: bold;
}

.student-info {
  flex: 1;
}

.student-info h2 {
  margin-top: 0;
  margin-bottom: 20px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 18px;
}

.info-grid span,
.booking-details span,
.payment-grid span {
  display: block;
  color: #777;
  font-size: 13px;
  margin-bottom: 5px;
}

.section {
  margin-top: 30px;
}

.section h2 {
  margin-bottom: 5px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.section-header p {
  color: #777;
}

.booking-count {
  background: #eee;
  padding: 7px 12px;
  border-radius: 20px;
  font-size: 14px;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 15px;
  margin-top: 20px;
}

.summary-card {
  background: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.summary-card span {
  display: block;
  color: #777;
  font-size: 14px;
}

.summary-card strong {
  display: block;
  font-size: 25px;
  margin-top: 8px;
}

.booking-list {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.booking-card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

.booking-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  border-bottom: 1px solid #eee;
  padding-bottom: 18px;
}

.booking-header h3 {
  margin: 0 0 6px;
}

.booking-header p {
  margin: 0;
  color: #777;
}

.status {
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 13px;
  text-transform: capitalize;
}

.status.confirmed {
  background: #dff6e5;
  color: #187a3d;
}

.status.pending {
  background: #fff3cd;
  color: #856404;
}

.status.cancelled {
  background: #f8d7da;
  color: #842029;
}

.status.completed {
  background: #dbeafe;
  color: #1d4ed8;
}

.booking-details {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  padding: 20px 0;
}

.payment {
  border-top: 1px solid #eee;
  padding-top: 18px;
}

.payment h4 {
  margin-top: 0;
}

.payment-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
}

.empty,
.loading,
.error {
  background: white;
  padding: 30px;
  margin-top: 20px;
  border-radius: 10px;
  text-align: center;
}

.error {
  color: #b42318;
}

@media (max-width: 1000px) {

  .summary-grid {
    grid-template-columns: repeat(3, 1fr);
  }

  .info-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .booking-details {
    grid-template-columns: repeat(2, 1fr);
  }

  .payment-grid {
    grid-template-columns: repeat(2, 1fr);
  }

}

@media (max-width: 600px) {

  .page {
    padding: 15px;
  }

  .student-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .summary-grid,
  .info-grid,
  .booking-details,
  .payment-grid {
    grid-template-columns: 1fr;
  }

  .header {
    align-items: flex-start;
    gap: 15px;
  }

}

</style>