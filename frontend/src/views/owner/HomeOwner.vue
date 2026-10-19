<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const stats = ref({
  properties: 0,
  rooms: 0,
  bookings: 0,
  earnings: 0,
  upcomingBookings: 0
})

const recentBookings = ref([])
const loading = ref(false)
const error = ref('')

const fetchDashboard = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch(
      'http://127.0.0.1:5000/api/owner/dashboard',
      {
        method: 'GET',
        headers: {
          'Authentication-Token': authStore.token
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      error.value = data.message || 'Failed to load dashboard.'
      return
    }

    stats.value.properties = data.dashboard.total_properties
    stats.value.rooms = data.dashboard.total_rooms
    stats.value.bookings = data.dashboard.total_bookings
    stats.value.earnings = data.dashboard.total_earnings
    stats.value.upcomingBookings = data.dashboard.upcoming_bookings

    recentBookings.value = data.dashboard.recent_bookings

  } catch (err) {
    console.error(err)
    error.value = 'Unable to connect to server.'
  } finally {
    loading.value = false
  }
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

const formatAmount = (amount) => {
  return Number(amount).toLocaleString('en-IN')
}

onMounted(() => {
  fetchDashboard()
})
</script>

<template>
  <div class="owner-page">

    <main class="dashboard">

      <div v-if="error" class="error">
        {{ error }}
      </div>

      <div v-if="loading" class="loading">
        Loading dashboard...
      </div>

      <template v-else>

        <section class="welcome-card">

          <div>
            <p class="welcome-label">EXAMSTAY OWNER</p>
            <h2>Welcome back 👋</h2>

            <p>
              Manage your properties, rooms and student bookings
              from one place.
            </p>
          </div>

          <RouterLink
            to="/owner/properties/add"
            class="welcome-btn"
          >
            List a Property
          </RouterLink>

        </section>


        <section class="stats-grid">

          <div class="stat-card">
            <div class="stat-icon">🏠</div>

            <div class="stat-content">
              <span>Total Properties</span>
              <strong>{{ stats.properties }}</strong>
            </div>
          </div>


          <div class="stat-card">
            <div class="stat-icon">🛏️</div>

            <div class="stat-content">
              <span>Total Rooms</span>
              <strong>{{ stats.rooms }}</strong>
            </div>
          </div>


          <div class="stat-card">
            <div class="stat-icon">📋</div>

            <div class="stat-content">
              <span>Total Bookings</span>
              <strong>{{ stats.bookings }}</strong>
            </div>
          </div>


          <div class="stat-card">
            <div class="stat-icon">₹</div>

            <div class="stat-content">
              <span>Total Earnings</span>
              <strong>₹{{ formatAmount(stats.earnings) }}</strong>
            </div>
          </div>

        </section>


        <section class="overview-card">

          <div class="overview-left">
            <span>Upcoming Bookings</span>
            <strong>{{ stats.upcomingBookings }}</strong>
            <p>Bookings scheduled for upcoming stays</p>
          </div>

          <RouterLink
            to="/owner/bookings"
            class="overview-btn"
          >
            View Bookings
          </RouterLink>

        </section>


        <section class="content-grid">

          <div class="main-card">

            <div class="card-header">
              <div>
                <p class="section-label">MANAGEMENT</p>
                <h2>Quick Actions</h2>
                <p>Frequently used owner actions</p>
              </div>
            </div>


            <div class="actions-grid">

              <RouterLink
                to="/owner/properties/add"
                class="action-card"
              >
                <span class="action-icon">🏠</span>

                <div>
                  <h3>Add Property</h3>
                  <p>List a new accommodation</p>
                </div>

                <span class="arrow">→</span>
              </RouterLink>


              <RouterLink
                to="/owner/properties"
                class="action-card"
              >
                <span class="action-icon">🏢</span>

                <div>
                  <h3>My Properties</h3>
                  <p>View and manage properties</p>
                </div>

                <span class="arrow">→</span>
              </RouterLink>


              <RouterLink
                to="/owner/bookings"
                class="action-card"
              >
                <span class="action-icon">📋</span>

                <div>
                  <h3>Bookings</h3>
                  <p>Manage student bookings</p>
                </div>

                <span class="arrow">→</span>
              </RouterLink>


              <RouterLink
                to="/owner/profile"
                class="action-card"
              >
                <span class="action-icon">👤</span>

                <div>
                  <h3>My Profile</h3>
                  <p>Update your owner details</p>
                </div>

                <span class="arrow">→</span>
              </RouterLink>

            </div>

          </div>


          <div class="side-card">

            <div class="card-header">
              <p class="section-label">ACTIVITY</p>
              <h2>Recent Bookings</h2>
              <p>Your latest student bookings</p>
            </div>


            <div
              v-if="recentBookings.length === 0"
              class="empty-state"
            >

              <div class="empty-icon">📋</div>

              <h3>No bookings yet</h3>

              <p>
                Your recent student bookings will appear here.
              </p>

            </div>


            <div
              v-else
              class="booking-list"
            >

              <div
                v-for="booking in recentBookings"
                :key="booking.booking_id"
                class="booking-item"
              >

                <div class="booking-top">

                  <div>
                    <strong>
                      Booking #{{ booking.booking_id }}
                    </strong>

                    <span>
                      Room #{{ booking.room_id }}
                    </span>
                  </div>

                  <span
                    class="status"
                    :class="booking.status"
                  >
                    {{ booking.status }}
                  </span>

                </div>


                <div class="booking-details">

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
                    <span>Guests</span>
                    <strong>
                      {{ booking.number_of_guests }}
                    </strong>
                  </div>

                </div>


                <div class="booking-bottom">

                  <span>
                    ₹{{ formatAmount(booking.total_amount) }}
                  </span>

                  <span>
                    {{ formatDate(booking.created_at) }}
                  </span>

                </div>

              </div>

            </div>

          </div>

        </section>

      </template>

    </main>

  </div>
</template>

<style scoped>

.owner-page {
  min-height: calc(100vh - 70px);
  background: #f7f7f7;
}

.owner-header {
  background: white;
  padding: 28px 50px;
  border-bottom: 1px solid #e5e5e5;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.label,
.section-label,
.welcome-label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  color: #777;
  margin: 0 0 8px;
}

.owner-header h1 {
  margin: 0 0 6px;
  font-size: 28px;
  color: #171717;
}

.owner-header p:last-child {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.add-btn {
  padding: 11px 20px;
  background: #171717;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
}

.add-btn:hover {
  background: #333;
}

.dashboard {
  max-width: 1250px;
  margin: auto;
  padding: 35px 30px;
}

.welcome-card {
  padding: 30px;
  background: #171717;
  color: white;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 25px;
}

.welcome-label {
  color: #999;
}

.welcome-card h2 {
  margin: 0 0 8px;
  font-size: 24px;
}

.welcome-card p:last-child {
  margin: 0;
  color: #ccc;
  font-size: 14px;
}

.welcome-btn {
  padding: 12px 20px;
  background: white;
  color: #171717;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 9px;
  padding: 22px;
  display: flex;
  align-items: center;
  gap: 15px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  flex-shrink: 0;
  background: #f1f1f1;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
}

.stat-content span {
  display: block;
  color: #777;
  font-size: 13px;
  margin-bottom: 5px;
}

.stat-content strong {
  font-size: 24px;
  color: #171717;
}

.overview-card {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 9px;
  padding: 22px 25px;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.overview-left span {
  display: block;
  color: #777;
  font-size: 13px;
  margin-bottom: 5px;
}

.overview-left strong {
  display: block;
  font-size: 28px;
  color: #171717;
  margin-bottom: 3px;
}

.overview-left p {
  margin: 0;
  color: #777;
  font-size: 12px;
}

.overview-btn {
  padding: 10px 18px;
  border: 1px solid #ccc;
  border-radius: 6px;
  color: #171717;
  text-decoration: none;
  font-size: 13px;
  font-weight: 600;
}

.content-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 25px;
}

.main-card,
.side-card {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 9px;
  padding: 25px;
}

.card-header {
  margin-bottom: 20px;
}

.card-header h2 {
  margin: 0 0 5px;
  font-size: 20px;
  color: #171717;
}

.card-header p:last-child {
  margin: 0;
  color: #777;
  font-size: 13px;
}

.actions-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.action-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 18px;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
  text-decoration: none;
  color: #171717;
}

.action-card:hover {
  border-color: #999;
}

.action-icon {
  font-size: 24px;
}

.action-card h3 {
  margin: 0 0 4px;
  font-size: 15px;
}

.action-card p {
  margin: 0;
  color: #777;
  font-size: 12px;
}

.arrow {
  margin-left: auto;
  font-size: 20px;
  color: #777;
}

.empty-state {
  text-align: center;
  padding: 55px 15px;
}

.empty-icon {
  font-size: 35px;
  margin-bottom: 12px;
}

.empty-state h3 {
  margin: 0 0 7px;
  font-size: 16px;
}

.empty-state p {
  margin: 0;
  color: #777;
  font-size: 13px;
  line-height: 1.5;
}

.booking-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.booking-item {
  padding: 15px;
  border: 1px solid #e5e5e5;
  border-radius: 8px;
}

.booking-top {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  margin-bottom: 14px;
}

.booking-top strong {
  display: block;
  font-size: 14px;
}

.booking-top span:not(.status) {
  display: block;
  color: #777;
  font-size: 12px;
  margin-top: 3px;
}

.status {
  height: fit-content;
  padding: 4px 8px;
  border-radius: 4px;
  background: #f1f1f1;
  font-size: 11px;
  text-transform: capitalize;
}

.booking-details {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 10px;
  padding-bottom: 12px;
  border-bottom: 1px solid #eee;
}

.booking-details span {
  display: block;
  color: #888;
  font-size: 10px;
  margin-bottom: 3px;
}

.booking-details strong {
  font-size: 12px;
}

.booking-bottom {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
  color: #777;
  font-size: 11px;
}

.booking-bottom span:first-child {
  color: #171717;
  font-weight: 600;
  font-size: 13px;
}

.error {
  padding: 12px 15px;
  margin-bottom: 20px;
  background: #fee;
  color: #b00020;
  border-radius: 6px;
}

.loading {
  padding: 60px;
  text-align: center;
  color: #777;
}

@media (max-width: 900px) {

  .stats-grid {
    grid-template-columns: 1fr 1fr;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }

}

@media (max-width: 650px) {

  .owner-header {
    padding: 22px;
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }

  .dashboard {
    padding: 25px 15px;
  }

  .welcome-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .actions-grid {
    grid-template-columns: 1fr;
  }

  .overview-card {
    align-items: flex-start;
    gap: 15px;
    flex-direction: column;
  }

  .booking-details {
    grid-template-columns: 1fr;
  }

}

</style>