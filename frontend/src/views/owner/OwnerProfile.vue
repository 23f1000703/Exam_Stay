<template>
  <div class="page">

    <div class="header">
      <div>
        <h1>My Profile</h1>
        <p>Manage your owner profile information</p>
      </div>

      <button @click="router.push('/owner/dashboard')">
        ← Dashboard
      </button>
    </div>

    <div v-if="loading" class="loading">
      Loading profile...
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div v-if="owner && !loading">

      <section class="profile-card">

        <div class="profile-top">

          <div class="avatar">
            <img
              v-if="owner.profile_photo"
              :src="imageUrl(owner.profile_photo)"
              alt="Profile"
            >

            <span v-else>
              {{ owner.name ? owner.name.charAt(0).toUpperCase() : 'O' }}
            </span>
          </div>

          <div class="profile-heading">
            <h2>{{ owner.name }}</h2>
            <p>{{ owner.email }}</p>

            <span class="role-badge">
              Property Owner
            </span>
          </div>

        </div>

      </section>

      <section class="card">

        <h2>Personal Information</h2>

        <div class="info-grid">

          <div class="info">
            <label>Full Name</label>
            <p>{{ owner.name || '-' }}</p>
          </div>

          <div class="info">
            <label>Email</label>
            <p>{{ owner.email || '-' }}</p>
          </div>

          <div class="info">
            <label>Mobile Number</label>
            <p>{{ owner.mobile || '-' }}</p>
          </div>

          <div class="info">
            <label>Owner ID</label>
            <p>{{ owner.id || '-' }}</p>
          </div>

          <div class="info">
            <label>User ID</label>
            <p>{{ owner.user_id || '-' }}</p>
          </div>

        </div>

      </section>

      <section class="card">

        <h2>Identity Information</h2>

        <div class="info-grid">

          <div class="info">
            <label>ID Type</label>
            <p>{{ owner.id_type || '-' }}</p>
          </div>

          <div class="info">
            <label>ID Number</label>
            <p>{{ owner.id_number || '-' }}</p>
          </div>

        </div>

      </section>

      <section class="card">

        <h2>Permanent Address</h2>

        <div class="address">

          <div class="info full">
            <label>Address</label>
            <p>{{ owner.property_address || '-' }}</p>
          </div>

          <div class="info">
            <label>District</label>
            <p>{{ owner.per_district || '-' }}</p>
          </div>

          <div class="info">
            <label>State</label>
            <p>{{ owner.per_state || '-' }}</p>
          </div>

          <div class="info">
            <label>Pincode</label>
            <p>{{ owner.per_pincode || '-' }}</p>
          </div>

        </div>

      </section>

      <section class="card">

        <h2>Account Information</h2>

        <div class="info-grid">

          <div class="info">
            <label>Profile Created</label>
            <p>{{ formatDate(owner.created_at) }}</p>
          </div>

          <div class="info">
            <label>Last Updated</label>
            <p>{{ formatDate(owner.updated_at) }}</p>
          </div>

        </div>

      </section>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const API = 'http://127.0.0.1:5000/api'
const SERVER = 'http://127.0.0.1:5000'

const owner = ref(null)
const loading = ref(true)
const error = ref('')

const fetchProfile = async () => {

  loading.value = true
  error.value = ''

  try {

    const response = await fetch(
      `${API}/owner/profile`,
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
        data.message || 'Failed to load profile.'
      return
    }

    owner.value = data.owner

  } catch (err) {

    console.error(err)

    error.value =
      'Unable to connect to server.'

  } finally {

    loading.value = false

  }
}

const imageUrl = (url) => {

  if (!url) return ''

  if (url.startsWith('http')) {
    return url
  }

  return `${SERVER}${url}`
}

const formatDate = (date) => {

  if (!date) return '-'

  return new Date(date).toLocaleDateString(
    'en-IN',
    {
      day: '2-digit',
      month: 'long',
      year: 'numeric'
    }
  )
}

onMounted(() => {
  fetchProfile()
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

.header button {
  padding: 10px 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 7px;
  cursor: pointer;
}

.profile-card {
  background: white;
  border-radius: 14px;
  padding: 28px;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,.05);
}

.profile-top {
  display: flex;
  align-items: center;
  gap: 20px;
}

.avatar {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: #222;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  font-size: 35px;
  font-weight: 700;
}

.avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-heading h2 {
  margin: 0 0 5px;
  font-size: 25px;
}

.profile-heading p {
  margin: 0 0 10px;
  color: #666;
}

.role-badge {
  display: inline-block;
  padding: 5px 10px;
  background: #eee;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 25px;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,.05);
}

.card h2 {
  margin-top: 0;
  margin-bottom: 20px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.address {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.info.full {
  grid-column: 1 / -1;
}

.info label {
  display: block;
  color: #777;
  font-size: 13px;
  margin-bottom: 5px;
}

.info p {
  margin: 0;
  font-size: 15px;
  font-weight: 500;
  word-break: break-word;
}

.loading {
  padding: 40px;
  text-align: center;
  color: #777;
}

.error {
  padding: 14px;
  background: #ffe8e8;
  color: #b42318;
  border-radius: 8px;
  margin-bottom: 20px;
}

@media (max-width: 700px) {

  .page {
    padding: 15px;
  }

  .info-grid,
  .address {
    grid-template-columns: 1fr;
  }

  .profile-top {
    align-items: flex-start;
  }

}
</style>