<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const property = ref(null)
const owner = ref(null)
const rooms = ref([])
const images = ref([])
const bookingSummary = ref({})
const bookings = ref([])

const loading = ref(false)
const error = ref('')
const verifyLoading = ref(false)
const verificationMessage = ref('')
const verificationError = ref('')

const getImageUrl = (url) => {
  if (!url) return ''

  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }

  return `http://localhost:5000${url.startsWith('/') ? '' : '/'}${url}`
}

const verifyProperty = async () => {
  try {
    verifyLoading.value = true
    verificationMessage.value = ''
    verificationError.value = ''

    const propertyId = route.params.property_id

    const response = await fetch(
      `http://localhost:5000/api/admin/properties/${propertyId}`,
      {
        method: 'PUT',
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
        `Invalid server response. HTTP ${response.status}`
      )
    }

    if (!response.ok) {
      throw new Error(
        data.message || 'Failed to verify property.'
      )
    }

    // Update the page immediately after database success
    property.value.verification_status =
      data.property.verification_status

    verificationMessage.value = data.message

  } catch (err) {
    console.error('Verification error:', err)
    verificationError.value =
      err.message || 'Unable to verify property.'
  } finally {
    verifyLoading.value = false
  }
}


const fetchPropertyDetails = async () => {
  try {
    loading.value = true
    error.value = ''

    const propertyId = route.params.property_id

    const response = await fetch(
      `http://localhost:5000/api/admin/properties/${propertyId}`,
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
        `Invalid server response. HTTP ${response.status}. Check API route or authentication.`
      )
    }

    if (!response.ok) {
      throw new Error(
        data.message || 'Failed to fetch property details.'
      )
    }

    property.value = data.property || null
    owner.value = data.owner || null
    rooms.value = data.rooms || []
    images.value = data.images || []
    bookingSummary.value = data.booking_summary || {}
    bookings.value = data.bookings || []

  } catch (err) {
    console.error('Property detail error:', err)
    error.value = err.message || 'Unable to load property details.'
  } finally {
    loading.value = false
  }
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

const formatAmount = (amount) => {
  if (amount === null || amount === undefined) {
    return 'N/A'
  }

  return new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 2
  }).format(amount)
}

const statusClass = (value) => {
  const normalized = (value || 'unknown')
    .toLowerCase()
    .replaceAll(' ', '-')

  if (
    ['pending', 'verified', 'rejected', 'confirmed',
      'cancelled', 'completed'].includes(normalized)
  ) {
    return normalized
  }

  return 'other'
}

const goBack = () => {
  router.push('/admin/properties')
}

onMounted(fetchPropertyDetails)
</script>
<template>
  <div class="detail-page">

    <header class="page-header">
      <div>
        <p class="eyebrow">EXAMSTAY ADMIN</p>
        <h1>Property Details</h1>
        <p class="subtitle">
          Review property information, owner, rooms and bookings.
        </p>
      </div>

      <button class="secondary-btn" @click="goBack">
        ← Back to Properties
      </button>
    </header>
<div v-if="loading" class="state-box">
      Loading property details...
    </div>
<div v-else-if="error" class="state-box error">
      <p>{{ error }}</p>
      <button class="secondary-btn" @click="fetchPropertyDetails">
        Try Again
      </button>
    </div>
<template v-else-if="property">
<section class="card overview-card">
        <div class="overview-top">
          <div>
            <p class="section-label">
              PROPERTY ID: {{ property.id }}
            </p>
            <h2>{{ property.name }}</h2>
            <p class="muted">
              {{ property.address || 'Address unavailable' }}
            </p>
            <p class="muted">
              {{ property.city || '' }}
              {{ property.district ? ', ' + property.district : '' }}
              {{ property.state ? ', ' + property.state : '' }}
              {{ property.pincode ? ' - ' + property.pincode : '' }}
            </p>
          </div>

          <span
            class="status"
            :class="statusClass(property.verification_status)"
          >
            {{ property.verification_status || 'Unknown' }}
          </span>
        </div>

          <div v-if="property.verification_status?.toLowerCase() === 'pending'"
          class="verification-actions">
        <button
          class="verify-btn"
          :disabled="verifyLoading"
          @click="verifyProperty"
        >
          {{ verifyLoading ? 'Verifying...' : '✓ Mark as Verified' }}
          </button>
        </div>

        <p v-if="verificationMessage" class="verification-success">
          {{ verificationMessage }}
        </p>

        <p v-if="verificationError" class="verification-error">
          {{ verificationError }}
        </p>

        <div class="divider"></div>

        <h3>Description</h3>
        <p class="description">
          {{ property.description || 'No description provided.' }}
        </p>

        <div class="metadata">
          <div>
            <span>Created</span>
            <strong>{{ formatDate(property.created_at) }}</strong>
          </div>
          <div>
            <span>Last updated</span>
            <strong>{{ formatDate(property.updated_at) }}</strong>
          </div>
          <div>
            <span>Latitude</span>
            <strong>{{ property.latitude ?? 'N/A' }}</strong>
          </div>
          <div>
            <span>Longitude</span>
            <strong>{{ property.longitude ?? 'N/A' }}</strong>
          </div>
        </div>
      </section>
<section class="summary-grid">
        <div class="summary-card">
          <span>Total bookings</span>
          <strong>{{ bookingSummary.total_bookings ?? 0 }}</strong>
        </div>
        <div class="summary-card">
          <span>Pending</span>
          <strong>{{ bookingSummary.pending ?? 0 }}</strong>
        </div>
        <div class="summary-card">
          <span>Confirmed</span>
          <strong>{{ bookingSummary.confirmed ?? 0 }}</strong>
        </div>
        <div class="summary-card">
          <span>Cancelled</span>
          <strong>{{ bookingSummary.cancelled ?? 0 }}</strong>
        </div>
        <div class="summary-card">
          <span>Completed</span>
          <strong>{{ bookingSummary.completed ?? 0 }}</strong>
        </div>
      </section>
<section class="card">
        <div class="section-heading">
          <h2>Owner Information</h2>
        </div>

        <div v-if="owner" class="info-grid">
          <div>
            <span>Owner name</span>
            <strong>{{ owner.name || 'N/A' }}</strong>
          </div>
          <div>
            <span>Email</span>
            <strong>{{ owner.email || 'N/A' }}</strong>
          </div>
          <div>
            <span>Mobile</span>
            <strong>{{ owner.mobile || 'N/A' }}</strong>
          </div>
          <div>
            <span>Owner ID</span>
            <strong>{{ owner.id ?? 'N/A' }}</strong>
          </div>
          <div>
            <span>User ID</span>
            <strong>{{ owner.user_id ?? 'N/A' }}</strong>
          </div>
          <div>
            <span>Owner's property address</span>
            <strong>{{ owner.property_address || 'N/A' }}</strong>
          </div>
        </div>

        <p v-else class="muted">No owner information available.</p>
      </section>
<section class="card">
        <div class="section-heading">
          <h2>Rooms</h2>
          <span class="count">{{ rooms.length }} rooms</span>
        </div>

        <div v-if="rooms.length" class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Room</th>
                <th>Type</th>
                <th>Capacity</th>
                <th>Price / Night</th>
                <th>Availability</th>
                <th>Amenities</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="room in rooms" :key="room.id">
                <td>
                  <strong>{{ room.room_number || 'N/A' }}</strong>
                  <small>ID: {{ room.id }}</small>
                </td>
                <td>{{ room.room_type || 'N/A' }}</td>
                <td>{{ room.capacity ?? 'N/A' }}</td>
                <td>{{ formatAmount(room.price_per_night) }}</td>
                <td>
                  <span
                    class="status"
                    :class="room.available ? 'verified' : 'rejected'"
                  >
                    {{ room.available ? 'Available' : 'Unavailable' }}
                  </span>
                </td>
                <td>
                  <div v-if="room.amenities?.length" class="amenity-list">
                    <span
                      v-for="amenity in room.amenities"
                      :key="amenity.id"
                      class="amenity"
                    >
                      {{ amenity.name }}
                    </span>
                  </div>
                  <span v-else class="muted">No amenities</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <p v-else class="empty-message">No rooms added to this property.</p>
      </section>
<section class="card">
        <div class="section-heading">
          <h2>Property Images</h2>
          <span class="count">{{ images.length }} images</span>
        </div>

        <div v-if="images.length" class="image-grid">
          <div
            v-for="image in images"
            :key="image.id"
            class="image-card"
          >
            <img
              :src="getImageUrl(image.image_url)"
              :alt="property.name"
              loading="lazy"
            />
            <div class="image-caption">
              <span>Image #{{ image.id }}</span>
              <span v-if="image.is_primary" class="primary-label">
                Primary
              </span>
            </div>
          </div>
        </div>

        <p v-else class="empty-message">No images uploaded.</p>
      </section>
<section class="card">
        <div class="section-heading">
          <h2>Booking History</h2>
          <span class="count">{{ bookings.length }} bookings</span>
        </div>

        <div v-if="bookings.length" class="table-wrapper">
          <table>
            <thead>
              <tr>
                <th>Booking ID</th>
                <th>Student</th>
                <th>Check-in</th>
                <th>Check-out</th>
                <th>Guests</th>
                <th>Amount</th>
                <th>Status</th>
                <th>Booked On</th>
              </tr>
            </thead>

            <tbody>
              <tr
                v-for="booking in bookings"
                :key="booking.id"
              >
                <td>#{{ booking.id }}</td>
                <td>
                  <strong>{{ booking.student_name || 'N/A' }}</strong>
                  <small>
                    Student ID: {{ booking.customer_id ?? 'N/A' }}
                  </small>
                </td>
                <td>{{ formatDate(booking.check_in) }}</td>
                <td>{{ formatDate(booking.check_out) }}</td>
                <td>{{ booking.number_of_guests ?? 'N/A' }}</td>
                <td>{{ formatAmount(booking.total_amount) }}</td>
                <td>
                  <span
                    class="status"
                    :class="statusClass(booking.status)"
                  >
                    {{ booking.status || 'Unknown' }}
                  </span>
                  

                  <p v-if="verificationMessage" class="verification-success">
                    {{ verificationMessage }}
                  </p>

                  <p v-if="verificationError" class="verification-error">
                    {{ verificationError }}
                  </p>

                </td>
                <td>{{ formatDate(booking.created_at) }}</td>
              </tr>
            </tbody>
          </table>
        </div>

        <p v-else class="empty-message">
          No bookings found for this property.
        </p>
      </section>

    </template>

    <div v-else class="state-box">
      Property details are unavailable.
    </div>

  </div>
</template>

<style scoped>
.detail-page {
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

h2 {
  margin: 0;
  font-size: 20px;
}

h3 {
  margin: 0 0 10px;
  font-size: 15px;
}

.card {
  margin-bottom: 22px;
  padding: 24px;
  background: white;
  border: 1px solid #e6e6e3;
  border-radius: 9px;
}

.overview-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 18px;
}

.overview-top h2 {
  margin-bottom: 10px;
  font-size: 26px;
}

.section-label {
  color: #777;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1px;
}

.muted,
.description {
  color: #737373;
  line-height: 1.6;
  overflow-wrap: anywhere;
}

.description {
  margin-bottom: 20px;
}

.divider {
  height: 1px;
  background: #eeeeeb;
  margin: 22px 0;
}

.metadata,
.info-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
}

.metadata > div,
.info-grid > div {
  min-width: 0;
}

.metadata span,
.info-grid span {
  display: block;
  margin-bottom: 7px;
  color: #777;
  font-size: 12px;
}

.metadata strong,
.info-grid strong {
  display: block;
  overflow-wrap: anywhere;
  font-size: 14px;
  font-weight: 600;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 14px;
  margin-bottom: 22px;
}

.summary-card {
  padding: 18px;
  background: white;
  border: 1px solid #e6e6e3;
  border-radius: 9px;
}

.summary-card span {
  display: block;
  color: #737373;
  font-size: 12px;
}

.summary-card strong {
  display: block;
  margin-top: 10px;
  font-size: 27px;
}

.section-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.count {
  color: #777;
  font-size: 13px;
}

.status {
  display: inline-block;
  padding: 6px 10px;
  border-radius: 20px;
  background: #eee;
  color: #555;
  font-size: 12px;
  text-transform: capitalize;
  white-space: nowrap;
}

.status.pending {
  background: #fff1ce;
  color: #805b00;
}

.status.verified,
.status.confirmed,
.status.completed {
  background: #e1f5e7;
  color: #176b35;
}

.status.rejected,
.status.cancelled {
  background: #fbe5e5;
  color: #a12727;
}

.table-wrapper {
  overflow-x: auto;
}

table {
  width: 100%;
  min-width: 850px;
  border-collapse: collapse;
  text-align: left;
}

th {
  padding: 14px;
  background: #fafaf9;
  color: #686868;
  font-size: 11px;
  text-transform: uppercase;
}

td {
  padding: 15px 14px;
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

.image-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
}

.image-card {
  overflow: hidden;
  border: 1px solid #e6e6e3;
  border-radius: 8px;
}

.image-card img {
  display: block;
  width: 100%;
  height: 190px;
  object-fit: cover;
  background: #f0f0ed;
}

.image-caption {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 8px;
  padding: 12px;
  font-size: 12px;
}

.primary-label {
  color: #176b35;
  font-weight: 700;
}

.amenity-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.amenity {
  padding: 9px 13px;
  background: #f3f3f0;
  border: 1px solid #e6e6e3;
  border-radius: 6px;
  font-size: 13px;
}

.secondary-btn,
.state-box button {
  padding: 11px 15px;
  background: white;
  border: 1px solid #d5d5d2;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}

.secondary-btn:hover {
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

.empty-message {
  padding: 18px 0;
  color: #777;
  font-size: 14px;
}

@media (max-width: 1000px) {
  .summary-grid {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .image-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 700px) {
  .detail-page {
    padding: 22px 15px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  h1 {
    font-size: 28px;
  }

  .card {
    padding: 18px;
  }

  .overview-top {
    flex-direction: column;
  }

  .metadata,
  .info-grid {
    grid-template-columns: 1fr;
  }

  .summary-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .image-grid {
    grid-template-columns: 1fr;
  }
  
  .verification-actions {
    margin-top: 20px;
  }

  .verify-btn {
    padding: 12px 18px;
    background: #176b35;
    color: white;
    border: none;
    border-radius: 6px;
    font-weight: 600;
    cursor: pointer;
  }

  .verify-btn:hover {
    background: #12552a;
  }

  .verify-btn:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }

  .verification-success {
    margin-top: 12px;
    color: #176b35;
    font-size: 14px;
  }

  .verification-error {
    margin-top: 12px;
    color: #a12727;
    font-size: 14px;
  }

}
</style>
