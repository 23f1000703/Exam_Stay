<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

const stats = ref({
  trips: 0,
  bookings: 0,
  upcoming_stays: 0
})

const studentName = ref('Student')
const loading = ref(false)
const errorMessage = ref('')

const fetchDashboard = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const response = await fetch(
      'http://localhost:5000/api/student/dashboard',
      {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authentication-Token': authStore.token
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(
        data.message || 'Failed to load dashboard.'
      )
    }

    studentName.value = data.student.name || 'Student'

    stats.value = {
      trips: data.stats.trips ?? 0,
      bookings: data.stats.bookings ?? 0,
      upcoming_stays: data.stats.upcoming_stays ?? 0
    }
  } catch (error) {
    console.error('Dashboard API error:', error)
    errorMessage.value = error.message || 'Unable to load dashboard.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchDashboard()
})
</script>

<template>
  <div class="student-page">

    <header class="student-header">
      <div>
        <h1>Student Dashboard</h1>
        <p>Plan your stay for your next exam or trip</p>
      </div>

      <RouterLink to="/student/profile" class="profile-btn">
        My Profile
      </RouterLink>
    </header>


    <main class="dashboard">

      <section class="welcome-card">

        <div>
          <span class="welcome-label">Welcome back</span>

          <h2>{{ studentName }} 👋</h2>

          <p>
            Find verified accommodation near your exam centre
            and manage your stays easily.
          </p>
        </div>

        <RouterLink
          to="/student/properties"
          class="search-btn"
        >
          Find a Stay
        </RouterLink>

      </section>


      <section class="stats-grid">

        <div class="stat-card">

          <div class="stat-icon">
            🎯
          </div>

          <div>
            <span>Exam Trips</span>
            <strong>{{ stats.trips }}</strong>
          </div>

        </div>


        <div class="stat-card">

          <div class="stat-icon">
            📋
          </div>

          <div>
            <span>Total Bookings</span>
            <strong>{{ stats.bookings }}</strong>
          </div>

        </div>


        <div class="stat-card">

          <div class="stat-icon">
            🏨
          </div>

          <div>
            <span>Upcoming Stays</span>
            <strong>{{ stats.upcoming_stays }}</strong>
          </div>

        </div>

      </section>


      <section class="content-grid">

        <div class="main-card">

          <div class="card-header">
            <div>
              <h2>Quick Actions</h2>
              <p>Manage your ExamStay activities</p>
            </div>
          </div>


          <div class="actions-grid">

            <RouterLink
              to="/student/properties"
              class="action-card"
            >

              <span class="action-icon">
                🔍
              </span>

              <div>
                <h3>Find Accommodation</h3>
                <p>
                  Search stays near your exam centre
                </p>
              </div>

              <span class="arrow">→</span>

            </RouterLink>


            <RouterLink
              to="/student/exam-trips"
              class="action-card"
            >

              <span class="action-icon">
                🎯
              </span>

              <div>
                <h3>Exam Trips</h3>
                <p>
                  Add and manage your exam trips
                </p>
              </div>

              <span class="arrow">→</span>

            </RouterLink>


            <RouterLink
              to="/student/bookings"
              class="action-card"
            >

              <span class="action-icon">
                📋
              </span>

              <div>
                <h3>My Bookings</h3>
                <p>
                  View your accommodation bookings
                </p>
              </div>

              <span class="arrow">→</span>

            </RouterLink>


            <RouterLink
              to="/student/profile"
              class="action-card"
            >

              <span class="action-icon">
                👤
              </span>

              <div>
                <h3>My Profile</h3>
                <p>
                  Manage your personal information
                </p>
              </div>

              <span class="arrow">→</span>

            </RouterLink>

          </div>

        </div>


        <div class="side-card">

          <div class="side-header">

            <div>
              <h2>Upcoming Stay</h2>
              <p>Your next accommodation</p>
            </div>

          </div>


          <div class="empty-state">

            <div class="empty-icon">
              🏨
            </div>

            <h3>No upcoming stay</h3>

            <p>
              Search for a verified accommodation
              near your exam centre.
            </p>

            <RouterLink
              to="/student/search"
              class="small-btn"
            >
              Find a Stay
            </RouterLink>

          </div>

        </div>

      </section>


      <section class="features-section">

        <h2>Why use ExamStay?</h2>

        <div class="features-grid">

          <div class="feature-card">
            <div class="feature-icon">✓</div>
            <h3>Verified Stays</h3>
            <p>
              Find verified accommodation options
              for your short-term stay.
            </p>
          </div>


          <div class="feature-card">
            <div class="feature-icon">📍</div>
            <h3>Near Your Exam Centre</h3>
            <p>
              Search accommodation based on
              your exam centre location.
            </p>
          </div>


          <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <h3>Secure Booking</h3>
            <p>
              Manage your bookings and stay details
              from your dashboard.
            </p>
          </div>

        </div>

      </section>

    </main>

  </div>
</template>


<style scoped>

.student-page {
  min-height: calc(100vh - 70px);
  background: #f7f7f7;
}


.student-header {
  background: white;
  padding: 28px 50px;
  border-bottom: 1px solid #e5e5e5;
  display: flex;
  align-items: center;
  justify-content: space-between;
}


.student-header h1 {
  margin: 0 0 6px;
  font-size: 28px;
  color: #171717;
}


.student-header p {
  margin: 0;
  color: #666;
  font-size: 14px;
}


.profile-btn {
  padding: 10px 18px;
  border: 1px solid #ddd;
  color: #171717;
  text-decoration: none;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 600;
}


.dashboard {
  max-width: 1250px;
  margin: auto;
  padding: 35px 30px;
}


.welcome-card {
  background: #171717;
  color: white;
  padding: 32px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 25px;
}


.welcome-label {
  font-size: 13px;
  color: #aaa;
}


.welcome-card h2 {
  margin: 6px 0 8px;
  font-size: 26px;
}


.welcome-card p {
  margin: 0;
  color: #ccc;
  font-size: 14px;
  max-width: 600px;
}


.search-btn {
  padding: 13px 22px;
  background: white;
  color: #171717;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 600;
  font-size: 14px;
  white-space: nowrap;
}


.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 25px;
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
  background: #f1f1f1;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 21px;
}


.stat-card span {
  display: block;
  color: #777;
  font-size: 13px;
  margin-bottom: 5px;
}


.stat-card strong {
  font-size: 24px;
  color: #171717;
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


.card-header h2,
.side-header h2 {
  margin: 0 0 5px;
  font-size: 20px;
  color: #171717;
}


.card-header p,
.side-header p {
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
  padding: 45px 15px;
}


.empty-icon {
  font-size: 38px;
  margin-bottom: 12px;
}


.empty-state h3 {
  margin: 0 0 8px;
  font-size: 16px;
}


.empty-state p {
  margin: 0 auto 18px;
  max-width: 230px;
  color: #777;
  font-size: 13px;
  line-height: 1.5;
}


.small-btn {
  display: inline-block;
  padding: 9px 16px;
  background: #171717;
  color: white;
  border-radius: 5px;
  text-decoration: none;
  font-size: 13px;
  font-weight: 600;
}


.features-section {
  margin-top: 25px;
}


.features-section > h2 {
  margin-bottom: 18px;
  font-size: 20px;
}


.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}


.feature-card {
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 9px;
  padding: 22px;
}


.feature-icon {
  font-size: 22px;
  margin-bottom: 12px;
}


.feature-card h3 {
  margin: 0 0 7px;
  font-size: 16px;
}


.feature-card p {
  margin: 0;
  color: #777;
  font-size: 13px;
  line-height: 1.5;
}


@media (max-width: 900px) {

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

}


@media (max-width: 650px) {

  .student-header {
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

  .actions-grid {
    grid-template-columns: 1fr;
  }

}

</style>