<script setup>
import { ref, onMounted } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const search = ref('')
const city = ref('')
const properties = ref([])
const loading = ref(false)
const errorMessage = ref('')
const imageErrors = ref({})
const API_BASE_URL = 'http://localhost:5000'

const fetchProperties = async () => {
  loading.value = true
  errorMessage.value = ''

  try {
    const params = new URLSearchParams()

    if (search.value.trim()) {
      params.set('search', search.value.trim())
    }

    if (city.value.trim()) {
      params.set('city', city.value.trim())
    }

    const queryString = params.toString()
    const url = `http://localhost:5000/api/student/properties${
      queryString ? `?${queryString}` : ''
    }`

    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.token
      }
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(
        data.message || 'Failed to fetch properties.'
      )
    }

    properties.value = data.properties || []
  } catch (error) {
    console.error('Property search error:', error)
    properties.value = []
    errorMessage.value =
      error.message || 'Unable to load properties.'
  } finally {
    loading.value = false
  }
}

const resetFilters = () => {
  search.value = ''
  city.value = ''
  fetchProperties()
}

const getImage = (property) => {
  if (!property.images?.length) return ''

  const primaryImage = property.images.find(
    (image) => image.is_primary
  )

  const imagePath = primaryImage?.image_url || property.images[0].image_url || ''
  if (!imagePath) return ''
  if (imagePath.startsWith('http://') || imagePath.startsWith('https://')) return imagePath
  return `${API_BASE_URL}${imagePath.startsWith('/') ? '' : '/'}${imagePath}`
}

const handleImageError = (propertyId) => {
  imageErrors.value = { ...imageErrors.value, [propertyId]: true }
}

const getRoomAmenities = (room) => {
  if (!Array.isArray(room.amenities)) return []
  return room.amenities
    .map((amenity) => typeof amenity === 'string' ? amenity : amenity?.name)
    .filter(Boolean)
}

const formatPrice = (price) => {
  return Number(price).toLocaleString('en-IN')
}

const viewProperty = (propertyId) => {
  router.push(`/student/properties/${propertyId}`)
}

onMounted(() => {
  fetchProperties()
})
</script>



<template>
  <div class="search-page">
    <header class="page-header">
      <div>
        <h1>Find Your Stay</h1>
        <p>Find verified hotels and PGs near your exam destination.</p>
      </div>

      <RouterLink to="/student" class="back-btn">
        Dashboard
      </RouterLink>
    </header>

    <section class="search-panel">
      <div class="filter-field">
        <label for="search">Hotel / PG name</label>
        <input
          id="search"
          v-model="search"
          type="text"
          placeholder="Search by property name"
          @keyup.enter="fetchProperties"
        />
      </div>

      <div class="filter-field">
        <label for="city">City</label>
        <input
          id="city"
          v-model="city"
          type="text"
          placeholder="Enter city, e.g. Patna"
          @keyup.enter="fetchProperties"
        />
      </div>

      <button
        class="search-btn"
        :disabled="loading"
        @click="fetchProperties"
      >
        {{ loading ? 'Searching...' : 'Search Stays' }}
      </button>

      <button class="reset-btn" @click="resetFilters">
        Reset
      </button>
    </section>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
      <button @click="fetchProperties">Try Again</button>
    </div>

    <section class="results-section">
      <div class="results-heading">
        <div>
          <h2>Verified Properties</h2>
          <p>Choose a stay that fits your needs and budget.</p>
        </div>

        <span class="result-count">
          {{ properties.length }} properties
        </span>
      </div>

      <div v-if="loading" class="state-message">
        Loading verified properties...
      </div>

      <div
        v-else-if="!errorMessage && properties.length === 0"
        class="state-message"
      >
        <h3>No properties found</h3>
        <p>Try another hotel name or city.</p>
      </div>

      <div v-else-if="!loading" class="property-grid">
        <article
          v-for="property in properties"
          :key="property.id"
          class="property-card"
        >
          <div class="property-image">
            <img
              v-if="getImage(property) && !imageErrors[property.id]"
              :src="getImage(property)"
              :alt="property.name"
              @error="handleImageError(property.id)"
            />

            <div v-else class="image-placeholder">
              <span>🏨</span>
              <p>No image available</p>
            </div>

            <span class="verified-badge">
              ✓ Verified
            </span>
          </div>

          <div class="property-content">
            <h3>{{ property.name }}</h3>

            <p class="property-location">
              📍
              {{ property.city || 'City not specified' }}
              <span v-if="property.state">
                , {{ property.state }}
              </span>
            </p>

            <p class="property-address">
              {{ property.address }}
            </p>

            <p class="property-description">
              {{ property.description || 'No description available.' }}
            </p>

            <div class="property-info">
              <span>
                🛏️ {{ property.available_rooms }}
                {{ property.available_rooms === 1 ? 'room' : 'rooms' }}
                available
              </span>
            </div>

            <div v-if="property.rooms?.length" class="room-amenities">
              <h4>Room Amenities</h4>
              <div
                v-for="room in property.rooms"
                :key="room.id"
                class="room-amenity-row"
              >
                <strong>Room {{ room.room_number || room.room_type || room.id }}</strong>
                <div v-if="getRoomAmenities(room).length" class="amenity-list">
                  <span
                    v-for="amenity in getRoomAmenities(room)"
                    :key="amenity"
                    class="amenity-pill"
                  >{{ amenity }}</span>
                </div>
                <span v-else class="no-amenities">No amenities listed</span>
              </div>
            </div>

            <div class="card-footer">
              <div class="price">
                <template v-if="property.starting_price != null">
                  <span class="price-label">Starting from</span>
                  <strong>
                    ₹{{ formatPrice(property.starting_price) }}
                  </strong>
                  <small>/ night</small>
                </template>

                <span v-else class="price-unavailable">
                  Price unavailable
                </span>
              </div>

              <button
                class="details-btn"
                :disabled="property.available_rooms === 0"
                @click="viewProperty(property.id)"
              >
                {{
                  property.available_rooms > 0
                    ? 'View Details'
                    : 'No Rooms'
                }}
              </button>
            </div>
          </div>
        </article>
      </div>
    </section>
  </div>
</template>



<style scoped>
.search-page {
  min-height: 100vh;
  padding: 32px;
  background: #f5f7fb;
  color: #1e293b;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  margin-bottom: 28px;
}

.page-header h1 {
  margin: 0 0 8px;
  font-size: 30px;
  font-weight: 750;
}

.page-header p,
.results-heading p {
  margin: 0;
  color: #64748b;
}

.back-btn {
  text-decoration: none;
  padding: 10px 18px;
  border: 1px solid #dbe2ea;
  border-radius: 8px;
  color: #334155;
  background: white;
}

.search-panel {
  display: flex;
  align-items: end;
  gap: 16px;
  flex-wrap: wrap;
  padding: 22px;
  background: white;
  border: 1px solid #e7ebf2;
  border-radius: 14px;
  margin-bottom: 32px;
}

.filter-field {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
  min-width: 200px;
}

.filter-field label {
  font-size: 13px;
  font-weight: 650;
  color: #475569;
}

.filter-field input {
  width: 100%;
  box-sizing: border-box;
  padding: 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  outline: none;
  font-size: 14px;
}

.filter-field input:focus {
  border-color: #2563eb;
}

.search-btn,
.reset-btn,
.details-btn {
  border: none;
  border-radius: 8px;
  padding: 12px 17px;
  cursor: pointer;
  font-weight: 650;
}

.search-btn,
.details-btn {
  background: #2563eb;
  color: white;
}

.search-btn:disabled,
.details-btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.reset-btn {
  background: #e2e8f0;
  color: #334155;
}

.results-heading {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 15px;
  margin-bottom: 22px;
}

.results-heading h2 {
  margin: 0 0 7px;
  font-size: 23px;
}

.result-count {
  padding: 8px 12px;
  border-radius: 20px;
  background: #e0e7ff;
  color: #3730a3;
  font-size: 13px;
  font-weight: 650;
  white-space: nowrap;
}

.property-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
  gap: 24px;
}

.property-card {
  overflow: hidden;
  background: white;
  border: 1px solid #e7ebf2;
  border-radius: 14px;
  transition: box-shadow 0.2s, transform 0.2s;
}

.property-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08);
}

.property-image {
  height: 200px;
  position: relative;
  background: #e2e8f0;
}

.property-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-placeholder {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #64748b;
}

.image-placeholder span {
  font-size: 38px;
}

.image-placeholder p {
  margin: 8px 0 0;
  font-size: 13px;
}

.verified-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 6px 10px;
  background: #dcfce7;
  color: #166534;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 700;
}

.property-content {
  padding: 18px;
}

.property-content h3 {
  margin: 0 0 10px;
  font-size: 19px;
}

.property-location {
  margin: 0 0 7px;
  color: #475569;
  font-size: 14px;
}

.property-address,
.property-description {
  font-size: 13px;
  line-height: 1.6;
  color: #64748b;
  overflow-wrap: anywhere;
}

.property-address {
  margin: 0 0 8px;
}

.property-description {
  min-height: 42px;
  margin: 0 0 14px;
}

.property-info {
  padding: 11px 0;
  border-top: 1px solid #edf0f5;
  border-bottom: 1px solid #edf0f5;
  color: #475569;
  font-size: 13px;
}


.room-amenities {
  padding-top: 14px;
}

.room-amenities h4 {
  margin: 0 0 10px;
  font-size: 14px;
  color: #334155;
}

.room-amenity-row {
  display: flex;
  flex-direction: column;
  gap: 7px;
  padding: 9px 0;
  border-bottom: 1px solid #edf0f5;
  font-size: 12px;
}

.room-amenity-row strong {
  color: #475569;
}

.amenity-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.amenity-pill {
  padding: 5px 8px;
  border-radius: 14px;
  background: #eff6ff;
  color: #1d4ed8;
  font-size: 11px;
}

.no-amenities {
  color: #94a3b8;
  font-size: 12px;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-top: 16px;
}

.price {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.price-label,
.price small {
  color: #64748b;
  font-size: 12px;
}

.price strong {
  font-size: 20px;
  color: #0f172a;
}

.price-unavailable {
  font-size: 12px;
  color: #64748b;
}

.details-btn {
  font-size: 13px;
  white-space: nowrap;
}

.state-message {
  padding: 50px 20px;
  text-align: center;
  color: #64748b;
  background: white;
  border: 1px solid #e7ebf2;
  border-radius: 12px;
}

.state-message h3 {
  color: #334155;
}

.error-message {
  padding: 16px;
  margin-bottom: 24px;
  color: #991b1b;
  background: #fee2e2;
  border-radius: 8px;
  overflow-wrap: anywhere;
}

.error-message button {
  margin-left: 12px;
  cursor: pointer;
}

@media (max-width: 600px) {
  .search-page {
    padding: 18px;
  }

  .page-header {
    align-items: flex-start;
  }

  .page-header h1 {
    font-size: 24px;
  }

  .search-panel {
    padding: 16px;
  }

  .filter-field {
    min-width: 100%;
  }

  .search-btn,
  .reset-btn {
    flex: 1;
  }

  .results-heading {
    align-items: flex-start;
  }

  .property-grid {
    grid-template-columns: 1fr;
  }
}
</style>
