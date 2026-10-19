<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const dashboard = ref({
  pending_owner_verification : 0,
  total_bookings: 0,
  total_owners: 0,
  total_properties: 0,
  total_students: 0
})

const loading = ref(true)
const error = ref('')

const fetchDashboard = async () => {
  try {
    loading.value = true
    error.value = ''

    const response = await fetch(
      'http://localhost:5000/api/admin/dashboard',
      {
        method: 'GET',
        headers: {
          'Authentication-Token': authStore.token
        }
      }
    )

    const data = await response.json()
    console.log('Dashboard data:', data)

    if (!response.ok) {
      throw new Error(
        data.message || 'Failed to load dashboard'
      )
    }

    dashboard.value = data

  } catch (err) {
    console.error(err)
    error.value = err.message || 'Unable to load dashboard'
  } finally {
    loading.value = false
  }
}

const logout = async () => {
  try {
    await fetch(
      'http://localhost:5000/api/logout',
      {
        method: 'POST',
        headers: {
          'Authentication-Token': authStore.token
        }
      }
    )
  } catch (err) {
    console.error(err)
  } finally {
    authStore.logout()
    router.push('/login')
  }
}

onMounted(() => {
  fetchDashboard()
})
</script>

<template>
  <div class="admin-page">

    <!-- Header -->
    <div class="admin-header">

      <div>
        <p class="label">EXAMSTAY ADMIN</p>

        <h1>Dashboard</h1>

        <p class="subtitle">
          Manage users, properties, bookings and verifications.
        </p>
      </div>

      <div class="header-actions">

        <button
          class="refresh-btn"
          @click="fetchDashboard"
          :disabled="loading"
        >
          {{ loading ? 'Refreshing...' : 'Refresh' }}
        </button>

        <button
          class="logout-btn"
          @click="logout"
        >
          Logout
        </button>

      </div>

    </div>


    <!-- Loading -->
    <div
      v-if="loading"
      class="state-box"
    >
      Loading dashboard...
    </div>


    <!-- Error -->
    <div
      v-else-if="error"
      class="error-box"
    >
      <span>{{ error }}</span>

      <button @click="fetchDashboard">
        Try Again
      </button>
    </div>


    <!-- Dashboard -->
    <template v-else>

      <!-- Statistics -->
      <div class="stats">

        <div class="stat-card">

          <span class="stat-label">
            Total Students
          </span>

          <strong>
            {{ dashboard.total_students }}
          </strong>

        </div>


        <div class="stat-card">

          <span class="stat-label">
            Total Owners
          </span>

          <strong>
            {{ dashboard.total_owners }}
          </strong>

        </div>


        <div class="stat-card">

          <span class="stat-label">
            Properties
          </span>

          <strong>
            {{ dashboard.total_properties }}
          </strong>

        </div>


        <div class="stat-card">

          <span class="stat-label">
            Bookings
          </span>

          <strong>
            {{ dashboard.total_bookings }}
          </strong>

        </div>


        <div class="stat-card pending">

          <span class="stat-label">
            Pending Verification
          </span>

          <strong>
            {{ dashboard.pending_owner_verification }}
          </strong>

        </div>

      </div>


      <!-- Quick Actions -->
      <div class="section-header">
        <div>
          <p class="section-label">
            MANAGEMENT
          </p>

          <h2>
            Quick Access
          </h2>
        </div>
      </div>


      <!-- Dashboard Cards -->
      <div class="dashboard-grid">

        <RouterLink
          to="/admin/Students"
          class="dashboard-card"
        >

          <div class="card-top">
            <div class="icon">
              01
            </div>

            <span class="arrow">
              →
            </span>
          </div>

          <h2>
            Users
          </h2>

          <p>
            View and manage registered students
            and accommodation owners.
          </p>

        </RouterLink>


        <RouterLink
          to="/admin/properties"
          class="dashboard-card"
        >

          <div class="card-top">
            <div class="icon">
              02
            </div>

            <span class="arrow">
              →
            </span>
          </div>

          <h2>
            Properties
          </h2>

          <p>
            Review, verify and manage listed
            accommodations.
          </p>

        </RouterLink>


        <RouterLink
          to="/admin/bookings"
          class="dashboard-card"
        >

          <div class="card-top">
            <div class="icon">
              03
            </div>

            <span class="arrow">
              →
            </span>
          </div>

          <h2>
            Bookings
          </h2>

          <p>
            View bookings and monitor
            accommodation reservations.
          </p>

        </RouterLink>


        <RouterLink
          to="/admin/verifications"
          class="dashboard-card"
        >

          <div class="card-top">
            <div class="icon">
              04
            </div>

            <span class="arrow">
              →
            </span>
          </div>

          <h2>
            Verifications
          </h2>

          <p>
            Review pending student and owner
            verification requests.
          </p>

        </RouterLink>


        <RouterLink
          to="/admin/complaints"
          class="dashboard-card"
        >

          <div class="card-top">
            <div class="icon">
              05
            </div>

            <span class="arrow">
              →
            </span>
          </div>

          <h2>
            Complaints
          </h2>

          <p>
            Review complaints and handle
            reported issues.
          </p>

        </RouterLink>


        <RouterLink
          to="/admin/reports"
          class="dashboard-card"
        >

          <div class="card-top">
            <div class="icon">
              06
            </div>

            <span class="arrow">
              →
            </span>
          </div>

          <h2>
            Reports
          </h2>

          <p>
            View platform activity and
            important reports.
          </p>

        </RouterLink>

      </div>

    </template>

  </div>
</template>


<style scoped>

.admin-page {
  min-height: calc(100vh - 70px);
  padding: 50px;
  background: #f7f7f5;
}


/* Header */

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 45px;
}

.label {
  margin: 0 0 10px;

  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;

  color: #666;
}

.admin-header h1 {
  margin: 0 0 10px;

  font-size: 42px;
  font-weight: 700;

  color: #171717;
}

.subtitle {
  margin: 0;

  color: #666;
  font-size: 15px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}


/* Buttons */

.refresh-btn,
.logout-btn {
  padding: 11px 20px;

  border: 1px solid #ccc;
  border-radius: 6px;

  background: white;

  cursor: pointer;

  font-size: 14px;
  font-weight: 600;

  transition: 0.2s;
}

.refresh-btn:hover,
.logout-btn:hover {
  border-color: #888;
  background: #fafafa;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.logout-btn {
  color: #222;
}


/* Statistics */

.stats {
  display: grid;

  grid-template-columns:
    repeat(5, minmax(0, 1fr));

  gap: 20px;

  margin-bottom: 50px;
}

.stat-card {
  padding: 25px;

  background: white;

  border: 1px solid #e5e5e5;

  border-radius: 8px;

  min-height: 120px;

  display: flex;
  flex-direction: column;
  justify-content: space-between;

  transition: 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
  border-color: #ccc;
}

.stat-card.pending {
  border-color: #e1d7bd;
  background: #fffdf7;
}

.stat-label {
  display: block;

  color: #666;

  font-size: 14px;
}

.stat-card strong {
  display: block;

  margin-top: 15px;

  font-size: 32px;

  color: #171717;
}


/* Section */

.section-header {
  margin-bottom: 20px;
}

.section-label {
  margin: 0 0 7px;

  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;

  color: #888;
}

.section-header h2 {
  margin: 0;

  font-size: 25px;

  color: #171717;
}


/* Dashboard Cards */

.dashboard-grid {
  display: grid;

  grid-template-columns:
    repeat(3, minmax(0, 1fr));

  gap: 20px;
}

.dashboard-card {
  padding: 30px;

  background: white;

  border: 1px solid #e5e5e5;

  border-radius: 8px;

  text-decoration: none;

  color: #171717;

  transition:
    transform 0.2s,
    border-color 0.2s,
    box-shadow 0.2s;
}

.dashboard-card:hover {
  transform: translateY(-4px);

  border-color: #aaa;

  box-shadow:
    0 8px 25px rgba(0, 0, 0, 0.05);
}

.card-top {
  display: flex;

  justify-content: space-between;

  align-items: center;

  margin-bottom: 25px;
}

.icon {
  font-size: 13px;

  font-weight: 700;

  color: #777;
}

.arrow {
  font-size: 20px;

  color: #999;

  transition: 0.2s;
}

.dashboard-card:hover .arrow {
  transform: translateX(4px);

  color: #222;
}

.dashboard-card h2 {
  margin: 0 0 10px;

  font-size: 22px;
}

.dashboard-card p {
  margin: 0;

  color: #666;

  line-height: 1.6;

  font-size: 14px;
}


/* Loading */

.state-box {
  padding: 60px;

  text-align: center;

  background: white;

  border: 1px solid #e5e5e5;

  border-radius: 8px;

  color: #666;
}


/* Error */

.error-box {
  display: flex;

  justify-content: space-between;

  align-items: center;

  gap: 20px;

  padding: 20px;

  background: #fff;

  border: 1px solid #e2caca;

  border-radius: 8px;

  color: #8a3333;
}

.error-box button {
  padding: 9px 16px;

  border: 1px solid #ccc;

  border-radius: 6px;

  background: white;

  cursor: pointer;

  font-weight: 600;
}


/* Tablet */

@media (max-width: 1200px) {

  .stats {
    grid-template-columns:
      repeat(3, minmax(0, 1fr));
  }

}


/* Small Tablet */

@media (max-width: 900px) {

  .admin-page {
    padding: 35px;
  }

  .admin-header {
    align-items: flex-start;

    gap: 25px;
  }

  .stats {
    grid-template-columns:
      repeat(2, minmax(0, 1fr));
  }

  .dashboard-grid {
    grid-template-columns:
      repeat(2, minmax(0, 1fr));
  }

}


/* Mobile */

@media (max-width: 600px) {

  .admin-page {
    padding: 25px 20px;
  }

  .admin-header {
    flex-direction: column;
  }

  .admin-header h1 {
    font-size: 34px;
  }

  .header-actions {
    width: 100%;
  }

  .refresh-btn,
  .logout-btn {
    flex: 1;
  }

  .stats {
    grid-template-columns: 1fr;
  }

  .dashboard-grid {
    grid-template-columns: 1fr;
  }

  .error-box {
    flex-direction: column;
    align-items: flex-start;
  }

}

</style>