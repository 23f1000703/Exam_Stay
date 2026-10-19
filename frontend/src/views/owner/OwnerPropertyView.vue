<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const property = ref(null)
const loading = ref(false)
const error = ref('')
const activeImage = ref(0)

const propertyId = route.params.property_id

const imageUrl = (url) => {
  if (!url) return ''
  return `http://127.0.0.1:5000${url}`
}

const fetchProperty = async () => {
  loading.value = true
  error.value = ''

  try {
    const response = await fetch(
      `http://127.0.0.1:5000/api/owner/properties/${propertyId}`,
      {
        method: 'GET',
        headers: {
          'Authentication-Token': authStore.token
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      error.value = data.message || 'Failed to load property.'
      return
    }

    property.value = data.property

  } catch (err) {
    console.error(err)
    error.value = 'Unable to connect to server.'
  } finally {
    loading.value = false
  }
}

const goBack = () => {
  router.push('/owner/properties')
}

const addRoom = () => {
  localStorage.setItem("current_property_id", String(propertyId))
  router.push("/owner/properties/add-room")
}

const addAmenities = () => {
  router.push(`/owner/properties/${propertyId}/amenities`)
}

const editProperty = () => {
  router.push(`/owner/properties/${propertyId}/edit`)
}

const manageImages = () => {
  router.push(`/owner/properties/${propertyId}/images`)
}

const formatPrice = (price) => {
  if (price === null || price === undefined) {
    return 'Not specified'
  }

  return `₹${Number(price).toLocaleString('en-IN')}`
}

const formatDate = (date) => {
  if (!date) {
    return 'Not available'
  }

  return new Date(date).toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  })
}

onMounted(() => {
  fetchProperty()
})
</script>

<template>
  <div class="page">

    <header class="header">

      <div>
        <p class="label">OWNER</p>
        <h1>Property Details</h1>
        <p class="subtitle">
          Complete information about your accommodation.
        </p>
      </div>

      <div class="header-actions">

        <button
          class="back-btn"
          @click="goBack"
        >
          ← Back
        </button>

        <button
          class="edit-btn"
          @click="editProperty"
        >
          Edit Property
        </button>

      </div>

    </header>

    <div
      v-if="error"
      class="error"
    >
      {{ error }}
    </div>

    <div
      v-if="loading"
      class="loading"
    >
      Loading property...
    </div>

    <main
      v-else-if="property"
      class="content"
    >

      <section class="hero-card">

        <div
          v-if="property.images && property.images.length"
          class="gallery"
        >

          <div class="main-image">

            <img
              :src="imageUrl(property.images[activeImage].image_url)"
              :alt="property.name"
            />

            <div class="image-number">
              {{ activeImage + 1 }} / {{ property.images.length }}
            </div>

          </div>

          <div class="thumbnails">

            <button
              v-for="(image, index) in property.images"
              :key="image.id"
              class="thumbnail"
              :class="{ active: activeImage === index }"
              @click="activeImage = index"
            >

              <img
                :src="imageUrl(image.image_url)"
                :alt="`Property image ${index + 1}`"
              />

              <span
                v-if="image.is_primary"
                class="primary-badge"
              >
                Primary
              </span>

            </button>

          </div>

        </div>

        <div
          v-else
          class="no-images"
        >

          <div class="no-image-icon">
            📷
          </div>

          <h3>No Photos Added</h3>

          <p>
            Add photos of your accommodation.
          </p>

          <button
            class="edit-btn"
            @click="manageImages"
          >
            Add Photos
          </button>

        </div>

      </section>

      <section class="property-title-card">

        <div class="title-content">

          <div>

            <p class="section-label">
              PROPERTY
            </p>

            <h2>
              {{ property.name }}
            </h2>

            <p
              v-if="property.description"
              class="description"
            >
              {{ property.description }}
            </p>

          </div>

          <span
            class="status"
            :class="property.verification_status"
          >
            {{ property.verification_status }}
          </span>

        </div>

      </section>

      <div class="grid">

        <section class="card">

          <p class="section-label">
            LOCATION
          </p>

          <h3>
            Property Address
          </h3>

          <div class="details">

            <div class="detail">
              <span>Address</span>
              <strong>{{ property.address }}</strong>
            </div>

            <div class="detail">
              <span>City</span>
              <strong>{{ property.city }}</strong>
            </div>

            <div class="detail">
              <span>District</span>
              <strong>{{ property.district }}</strong>
            </div>

            <div class="detail">
              <span>State</span>
              <strong>{{ property.state }}</strong>
            </div>

            <div class="detail">
              <span>Pincode</span>
              <strong>{{ property.pincode }}</strong>
            </div>

            <div
              v-if="property.latitude !== null && property.latitude !== undefined"
              class="detail"
            >
              <span>Latitude</span>
              <strong>{{ property.latitude }}</strong>
            </div>

            <div
              v-if="property.longitude !== null && property.longitude !== undefined"
              class="detail"
            >
              <span>Longitude</span>
              <strong>{{ property.longitude }}</strong>
            </div>

          </div>

        </section>

        <section class="card">

          <p class="section-label">
            VERIFICATION
          </p>

          <h3>
            Property Status
          </h3>

          <div class="verification">

            <div class="verification-icon">
              ✓
            </div>

            <div>
              <strong>
                {{ property.verification_status }}
              </strong>

              <p>
                Current verification status
              </p>
            </div>

          </div>

          <div class="details">

            <div class="detail">
              <span>Created</span>
              <strong>
                {{ formatDate(property.created_at) }}
              </strong>
            </div>

            <div class="detail">
              <span>Last Updated</span>
              <strong>
                {{ formatDate(property.updated_at) }}
              </strong>
            </div>

          </div>

        </section>

      </div>

      <section class="card">

        <div class="section-header">
          <div>
            <p class="section-label">ROOMS</p>
            <h3>Property Rooms</h3>
          </div>

          <div class="section-actions">
            <span class="count">
              {{ property.rooms?.length || 0 }}
            </span>

            <button class="edit-btn" @click="addRoom">
              + Add Room
            </button>
          </div>
        </div>

        <div
          v-if="property.rooms && property.rooms.length"
          class="room-grid"
        >

          <div
            v-for="room in property.rooms"
            :key="room.id"
            class="room-card"
          >

            <div class="room-header">

              <div>
                <span class="room-label">
                  ROOM
                </span>

                <h4>
                  {{ room.room_number }}
                </h4>
              </div>

              <span
                class="availability"
                :class="room.available ? 'available' : 'unavailable'"
              >
                {{ room.available ? 'Available' : 'Unavailable' }}
              </span>

            </div>

            <div class="room-details">

              <div>
                <span>Type</span>
                <strong>
                  {{ room.room_type }}
                </strong>
              </div>

              <div>
                <span>Capacity</span>
                <strong>
                  {{ room.capacity }} Person(s)
                </strong>
              </div>

              <div>
                <span>Price / Night</span>
                <strong>
                  {{ formatPrice(room.price_per_night) }}
                </strong>
              </div>

            </div>

          </div>

        </div>

        <div
          v-else
          class="empty"
        >
          No rooms have been added to this property.
        </div>

      </section>

      <section class="card">

        <div class="section-header">

          <div>
            <p class="section-label">
              AMENITIES
            </p>

            <h3>
              Property Amenities
            </h3>
          </div>

          <span class="count">
            {{ property.amenities?.length || 0 }}
          </span>

        </div>

        <div
          v-if="property.amenities && property.amenities.length"
          class="amenities"
        >

          <span
            v-for="amenity in property.amenities"
            :key="amenity.id"
            class="amenity"
          >
            {{ amenity.name }}
          </span>

        </div>

        <div
          v-else
          class="empty"
        >
          No amenities have been added.
        </div>

      </section>

      <section class="bottom-actions">

        <button
          class="secondary-btn"
          @click="manageImages"
        >
          Manage Photos
        </button>

        <button
          class="edit-btn"
          @click="editProperty"
        >
          Edit Property
        </button>

      </section>

    </main>

  </div>
</template>

<style scoped>
.page {
  min-height: 100vh;
  padding: 40px;
  background: #f5f7fa;
  color: #1f2937;
}

.header {
  max-width: 1150px;
  margin: 0 auto 28px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

.label,
.section-label {
  margin: 0 0 8px;
  color: #6b7280;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.4px;
}

.header h1 {
  margin: 0;
  color: #111827;
  font-size: 32px;
  font-weight: 700;
}

.subtitle {
  margin: 8px 0 0;
  color: #6b7280;
  font-size: 15px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.back-btn,
.secondary-btn,
.edit-btn {
  padding: 11px 18px;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.back-btn,
.secondary-btn {
  border: 1px solid #d1d5db;
  background: #ffffff;
  color: #374151;
}

.back-btn:hover,
.secondary-btn:hover {
  background: #f3f4f6;
}

.edit-btn {
  border: none;
  background: #111827;
  color: #ffffff;
}

.edit-btn:hover {
  background: #374151;
}

.error {
  max-width: 1150px;
  margin: 0 auto 20px;
  padding: 14px 16px;
  border: 1px solid #fecaca;
  border-radius: 8px;
  background: #fef2f2;
  color: #b91c1c;
  font-size: 14px;
}

.loading {
  max-width: 1150px;
  margin: 70px auto;
  text-align: center;
  color: #6b7280;
  font-size: 15px;
}

.content {
  max-width: 1150px;
  margin: 0 auto;
}

.hero-card,
.property-title-card,
.card {
  margin-bottom: 22px;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  background: #ffffff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}

.hero-card {
  overflow: hidden;
}

.gallery {
  padding: 18px;
}

.main-image {
  position: relative;
  width: 100%;
  height: 440px;
  overflow: hidden;
  border-radius: 10px;
  background: #f3f4f6;
}

.main-image img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

.image-number {
  position: absolute;
  right: 14px;
  bottom: 14px;
  padding: 6px 10px;
  border-radius: 6px;
  background: rgba(0, 0, 0, 0.65);
  color: #ffffff;
  font-size: 12px;
}

.thumbnails {
  margin-top: 14px;
  display: flex;
  gap: 10px;
  overflow-x: auto;
}

.thumbnail {
  position: relative;
  flex: 0 0 90px;
  width: 90px;
  height: 70px;
  padding: 0;
  overflow: hidden;
  border: 2px solid transparent;
  border-radius: 8px;
  background: #f3f4f6;
  cursor: pointer;
}

.thumbnail.active {
  border-color: #111827;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

.primary-badge {
  position: absolute;
  left: 4px;
  bottom: 4px;
  padding: 3px 5px;
  border-radius: 4px;
  background: #111827;
  color: #ffffff;
  font-size: 9px;
}

.no-images {
  padding: 70px 20px;
  text-align: center;
}

.no-image-icon {
  margin-bottom: 15px;
  font-size: 42px;
}

.no-images h3 {
  margin: 0 0 8px;
  color: #111827;
}

.no-images p {
  margin: 0 0 20px;
  color: #6b7280;
}

.property-title-card {
  padding: 28px;
}

.title-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

.property-title-card h2 {
  margin: 0;
  color: #111827;
  font-size: 28px;
}

.description {
  max-width: 750px;
  margin: 10px 0 0;
  color: #6b7280;
  line-height: 1.6;
  font-size: 14px;
}

.status {
  flex-shrink: 0;
  padding: 7px 12px;
  border-radius: 20px;
  background: #f3f4f6;
  color: #374151;
  font-size: 12px;
  font-weight: 700;
  text-transform: capitalize;
}

.status.pending {
  background: #fff7ed;
  color: #c2410c;
}

.status.approved {
  background: #ecfdf5;
  color: #047857;
}

.status.rejected {
  background: #fef2f2;
  color: #b91c1c;
}

.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 22px;
}

.card {
  padding: 26px;
}

.card h3 {
  margin: 0 0 20px;
  color: #111827;
  font-size: 20px;
}

.details {
  display: flex;
  flex-direction: column;
}

.detail {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 13px 0;
  border-bottom: 1px solid #f0f0f0;
}

.detail:last-child {
  border-bottom: none;
}

.detail span {
  color: #6b7280;
  font-size: 14px;
}

.detail strong {
  max-width: 65%;
  color: #374151;
  font-size: 14px;
  font-weight: 600;
  text-align: right;
  word-break: break-word;
}

.verification {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 18px;
  padding: 15px;
  border-radius: 10px;
  background: #f9fafb;
}

.verification-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  border-radius: 50%;
  background: #111827;
  color: #ffffff;
  font-weight: 700;
}

.verification strong {
  color: #111827;
  font-size: 14px;
  text-transform: capitalize;
}

.verification p {
  margin: 4px 0 0;
  color: #6b7280;
  font-size: 12px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.section-header .section-label {
  margin-bottom: 6px;
}

.section-header h3 {
  margin-bottom: 0;
}

.count {
  min-width: 30px;
  padding: 6px 10px;
  border-radius: 20px;
  background: #f3f4f6;
  color: #374151;
  font-size: 12px;
  font-weight: 700;
  text-align: center;
}

.room-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 15px;
}

.room-card {
  padding: 18px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  background: #fafafa;
}

.room-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 18px;
}

.room-label {
  color: #9ca3af;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 1px;
}

.room-card h4 {
  margin: 4px 0 0;
  color: #111827;
  font-size: 18px;
}

.availability {
  padding: 5px 9px;
  border-radius: 15px;
  font-size: 11px;
  font-weight: 600;
}

.availability.available {
  background: #ecfdf5;
  color: #047857;
}

.availability.unavailable {
  background: #fef2f2;
  color: #b91c1c;
}

.room-details {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.room-details span {
  display: block;
  margin-bottom: 5px;
  color: #9ca3af;
  font-size: 11px;
}

.room-details strong {
  color: #374151;
  font-size: 13px;
}

.amenities {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.amenity {
  padding: 9px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 20px;
  background: #f9fafb;
  color: #374151;
  font-size: 13px;
  font-weight: 500;
}

.empty {
  padding: 25px;
  border-radius: 8px;
  background: #f9fafb;
  color: #9ca3af;
  text-align: center;
  font-size: 14px;
}

.bottom-actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-bottom: 30px;
}

@media (max-width: 900px) {
  .page {
    padding: 25px;
  }

  .grid {
    grid-template-columns: 1fr;
  }

  .main-image {
    height: 360px;
  }
}

@media (max-width: 650px) {
  .page {
    padding: 18px;
  }

  .header {
    flex-direction: column;
  }

  .header-actions {
    width: 100%;
  }

  .back-btn,
  .edit-btn {
    flex: 1;
  }

  .title-content {
    flex-direction: column;
  }

  .status {
    align-self: flex-start;
  }

  .property-title-card {
    padding: 20px;
  }

  .property-title-card h2 {
    font-size: 23px;
  }

  .main-image {
    height: 260px;
  }

  .card {
    padding: 20px;
  }

  .room-grid {
    grid-template-columns: 1fr;
  }

  .room-details {
    grid-template-columns: 1fr;
  }

  .detail {
    flex-direction: column;
    gap: 5px;
  }

  .detail strong {
    max-width: 100%;
    text-align: left;
  }

  .bottom-actions {
    flex-direction: column;
  }

  .bottom-actions button {
    width: 100%;
  }
}
</style>