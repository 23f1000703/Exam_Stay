<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const authStore = useAuthStore()
const API_BASE_URL = 'http://localhost:5000'

const property = ref(null)
const loading = ref(false)
const submitting = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const selectedImage = ref('')
const imageErrors = ref({})
const selectedRoomId = ref('')
const checkIn = ref('')
const checkOut = ref('')
const guests = ref(1)

const propertyId = computed(() => route.params.id)
const images = computed(() => property.value?.images || [])
const rooms = computed(() => (property.value?.rooms || []).filter(room => room.available !== false))
const availableRooms = computed(() => rooms.value.length)
const startingPrice = computed(() => {
  const prices = rooms.value.map(room => Number(room.price_per_night)).filter(price => Number.isFinite(price) && price >= 0)
  return prices.length ? Math.min(...prices) : 0
})
const selectedRoom = computed(() => rooms.value.find(room => String(room.id) === String(selectedRoomId.value)))
const nights = computed(() => {
  if (!checkIn.value || !checkOut.value) return 0
  const start = new Date(`${checkIn.value}T00:00:00`)
  const end = new Date(`${checkOut.value}T00:00:00`)
  return Math.ceil((end - start) / 86400000)
})
const totalPrice = computed(() => {
  if (!selectedRoom.value || nights.value <= 0) return 0
  return Number(selectedRoom.value.price_per_night || 0) * nights.value
})
const mapUrl = computed(() => {
  if (!property.value) return ''
  if (property.value.latitude != null && property.value.longitude != null) {
    return `https://www.google.com/maps?q=${property.value.latitude},${property.value.longitude}`
  }
  const address = [property.value.address, property.value.city, property.value.district, property.value.state, property.value.pincode].filter(Boolean).join(', ')
  return `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(address)}`
})

const imageUrl = image => {
  const path = typeof image === 'string' ? image : image?.image_url
  if (!path) return ''
  if (path.startsWith('http://') || path.startsWith('https://')) return path
  return `${API_BASE_URL}${path.startsWith('/') ? '' : '/'}${path}`
}

const getAmenities = room => {
  if (!Array.isArray(room?.amenities)) return []
  return room.amenities.map(item => typeof item === 'string' ? item : item?.name).filter(Boolean)
}

const formatPrice = value => Number(value || 0).toLocaleString('en-IN')
const today = new Date()
const minDate = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`

const fetchProperty = async () => {
  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''
  property.value = null

  try {
    if (!authStore.token) throw new Error('Session expire ho gaya hai. Please dobara login karo.')
    if (!propertyId.value) throw new Error('Property ID URL mein nahi mila.')

    const response = await fetch(`${API_BASE_URL}/api/student/properties/${propertyId.value}`, {
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.token
      }
    })
    const data = await response.json()
    if (!response.ok) throw new Error(data.message || 'Property details load nahi ho paye.')

    const found = data.property
    if (!found) throw new Error('Property nahi mili ya verified nahi hai.')

    property.value = found
    const primary = found.images?.find(image => image.is_primary) || found.images?.[0]
    selectedImage.value = primary ? imageUrl(primary) : ''
    const firstRoom = (found.rooms || []).find(room => room.available !== false)
    selectedRoomId.value = firstRoom ? String(firstRoom.id) : ''
    guests.value = 1
  } catch (error) {
    errorMessage.value = error.message || 'Property details load nahi ho paye.'
  } finally {
    loading.value = false
  }
}

const chooseImage = image => {
  selectedImage.value = imageUrl(image)
}

const submitBooking = async () => {
  errorMessage.value = ''
  successMessage.value = ''

  if (!selectedRoom.value) {
    errorMessage.value = 'Please ek room select karo.'
    return
  }
  if (!checkIn.value || !checkOut.value) {
    errorMessage.value = 'Check-in aur check-out date select karo.'
    return
  }
  if (nights.value <= 0) {
    errorMessage.value = 'Check-out date, check-in ke baad honi chahiye.'
    return
  }
  if (Number(guests.value) < 1 || Number(guests.value) > Number(selectedRoom.value.capacity || 1)) {
    errorMessage.value = `Is room ki capacity ${selectedRoom.value.capacity || 1} guest hai.`
    return
  }

  submitting.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/api/student/bookings`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authentication-Token': authStore.token
      },
      body: JSON.stringify({
        property_id: Number(property.value.id),
        room_id: Number(selectedRoomId.value),
        check_in: checkIn.value,
        check_out: checkOut.value,
        number_of_guests: Number(guests.value)
      })
    })
    const data = await response.json()
    if (!response.ok) throw new Error(data.message || 'Booking request submit nahi ho payi.')
    successMessage.value = data.message || 'Booking request successfully submit ho gayi.'
  } catch (error) {
    errorMessage.value = error.message || 'Booking request submit nahi ho payi.'
  } finally {
    submitting.value = false
  }
}

watch(selectedRoomId, () => {
  if (selectedRoom.value && guests.value > Number(selectedRoom.value.capacity || 1)) {
    guests.value = Number(selectedRoom.value.capacity || 1)
  }
})

onMounted(fetchProperty)
</script>

<template>
  <main class="details-page">
    <header class="topbar">
      <RouterLink to="/student/properties" class="back-link">← Back to stays</RouterLink>
      <RouterLink to="/student" class="dashboard-link">Dashboard</RouterLink>
    </header>

    <div v-if="loading" class="state-card">Loading property details...</div>
    <div v-else-if="errorMessage && !property" class="state-card error-card">
      <p>{{ errorMessage }}</p>
      <button class="primary-btn" @click="fetchProperty">Try again</button>
    </div>

    <template v-else-if="property">
      <section class="property-heading">
        <div>
          <div class="badge-row"><span class="verified">✓ Verified property</span><span class="available">{{ availableRooms }} rooms available</span></div>
          <h1>{{ property.name }}</h1>
          <p class="location-line">📍 {{ [property.address, property.city, property.district, property.state, property.pincode].filter(Boolean).join(', ') || 'Location not provided' }}</p>
        </div>
        <a :href="mapUrl" target="_blank" rel="noopener noreferrer" class="map-btn">Open in Google Maps ↗</a>
      </section>

      <section class="gallery-section">
        <div class="main-photo">
          <img v-if="selectedImage && !imageErrors[selectedImage]" :src="selectedImage" :alt="property.name" @error="imageErrors[selectedImage] = true" />
          <div v-else class="photo-placeholder"><span>🏨</span><p>No photo available</p></div>
        </div>
        <div class="thumbnail-grid" v-if="images.length">
          <button v-for="image in images" :key="image.id || image.image_url" class="thumbnail" :class="{ active: selectedImage === imageUrl(image) }" @click="chooseImage(image)">
            <img :src="imageUrl(image)" :alt="`${property.name} photo`" @error="$event.target.style.visibility = 'hidden'" />
          </button>
        </div>
        <p v-else class="muted">Is property ke photos abhi available nahi hain.</p>
      </section>

      <div class="content-layout">
        <div class="main-column">
          <section class="info-card">
            <h2>About this stay</h2>
            <p class="description">{{ property.description || 'Property owner ne description add nahi kiya hai.' }}</p>
            <h3>Location & address</h3>
            <p>{{ [property.address, property.city, property.district, property.state, property.pincode].filter(Boolean).join(', ') || 'Address not provided' }}</p>
            <a :href="mapUrl" target="_blank" rel="noopener noreferrer" class="text-link">View location on map ↗</a>
          </section>

          <section class="info-card rooms-card">
            <h2>Available rooms</h2>
            <div v-if="rooms.length" class="room-list">
              <article v-for="room in rooms" :key="room.id" class="room-item" :class="{ 'room-selected': String(selectedRoomId) === String(room.id) }">
                <div class="room-topline">
                  <div><h3>{{ room.room_type || 'Room' }}</h3><p>Room {{ room.room_number || room.id }} <span v-if="room.capacity">· Up to {{ room.capacity }} guests</span></p></div>
                  <div class="room-price"><strong>₹{{ formatPrice(room.price_per_night) }}</strong><span>/ night</span></div>
                </div>
                <div class="amenity-list" v-if="getAmenities(room).length">
                  <span v-for="amenity in getAmenities(room)" :key="amenity" class="amenity-pill">{{ amenity }}</span>
                </div>
                <p v-else class="muted">Room amenities listed nahi hain.</p>
                <button class="select-room-btn" @click="selectedRoomId = String(room.id)">{{ String(selectedRoomId) === String(room.id) ? '✓ Selected' : 'Select this room' }}</button>
              </article>
            </div>
            <p v-else class="muted">Abhi koi available room nahi hai.</p>
          </section>
        </div>

        <aside class="booking-card">
          <div class="booking-title"><div><span class="muted">Starting from</span><h2>₹{{ formatPrice(startingPrice) }} <small>/ night</small></h2></div><span class="verified">Verified</span></div>
          <h3>Book your stay</h3>
          <form @submit.prevent="submitBooking">
            <label for="room">Choose room</label>
            <select id="room" v-model="selectedRoomId" required :disabled="!rooms.length">
              <option value="" disabled>Select a room</option>
              <option v-for="room in rooms" :key="room.id" :value="String(room.id)">{{ room.room_type }} · Room {{ room.room_number || room.id }} · ₹{{ formatPrice(room.price_per_night) }}/night</option>
            </select>

            <label for="check-in">Check-in</label>
            <input id="check-in" v-model="checkIn" type="date" :min="minDate" required />

            <label for="check-out">Check-out</label>
            <input id="check-out" v-model="checkOut" type="date" required :min="checkIn && checkIn >= minDate ? checkIn : minDate" />

            <label for="guests">Guests</label>
            <input id="guests" v-model.number="guests" type="number" min="1" :max="selectedRoom?.capacity || 1" required />

            <div v-if="nights > 0 && selectedRoom" class="price-breakdown">
              <div><span>₹{{ formatPrice(selectedRoom.price_per_night) }} × {{ nights }} nights</span><strong>₹{{ formatPrice(totalPrice) }}</strong></div>
              <small>Final confirmation availability verification ke baad hogi.</small>
            </div>

            <p v-if="errorMessage" class="form-message error-text">{{ errorMessage }}</p>
            <p v-if="successMessage" class="form-message success-text">{{ successMessage }}</p>
            <button class="primary-btn book-btn" type="submit" :disabled="submitting || !rooms.length">{{ submitting ? 'Submitting...' : 'Request Booking' }}</button>
          </form>
          <p class="booking-note">Booking request submit karne par status property owner ki confirmation ke liye pending rahega.</p>
        </aside>
      </div>
    </template>
  </main>
</template>

<style scoped>
*{box-sizing:border-box}.details-page{max-width:1200px;margin:0 auto;padding:28px 24px 60px;color:#172033}.topbar{display:flex;justify-content:space-between;align-items:center;margin-bottom:24px}.back-link,.dashboard-link,.text-link{color:#2457c5;text-decoration:none;font-weight:600}.property-heading{display:flex;justify-content:space-between;gap:20px;align-items:flex-end;margin-bottom:22px}.badge-row{display:flex;gap:9px;flex-wrap:wrap}.verified,.available{display:inline-flex;align-items:center;padding:6px 10px;border-radius:999px;font-size:12px;font-weight:700}.verified{color:#166534;background:#dcfce7}.available{color:#1d4ed8;background:#dbeafe}.property-heading h1{font-size:32px;margin:12px 0 8px}.location-line{color:#64748b;line-height:1.6;margin:0}.map-btn{white-space:nowrap;padding:11px 15px;border:1px solid #cbd5e1;border-radius:9px;color:#1e40af;text-decoration:none;font-weight:700}.gallery-section{display:grid;grid-template-columns:minmax(0,1.7fr) minmax(220px,1fr);gap:12px;margin-bottom:24px}.main-photo{height:390px;border-radius:15px;overflow:hidden;background:#e9eef5}.main-photo img{width:100%;height:100%;object-fit:cover}.photo-placeholder{height:100%;display:flex;align-items:center;justify-content:center;flex-direction:column;color:#64748b}.photo-placeholder span{font-size:50px}.thumbnail-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;align-content:start;max-height:390px;overflow:auto}.thumbnail{height:120px;padding:0;border:2px solid transparent;border-radius:10px;overflow:hidden;background:#eef2f7;cursor:pointer}.thumbnail.active{border-color:#2563eb}.thumbnail img{width:100%;height:100%;object-fit:cover}.content-layout{display:grid;grid-template-columns:minmax(0,1fr) 360px;gap:24px;align-items:start}.main-column{display:grid;gap:20px}.info-card,.booking-card{background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:24px;box-shadow:0 4px 16px rgba(15,23,42,.04)}.info-card h2{font-size:21px;margin:0 0 16px}.info-card h3{font-size:16px;margin:24px 0 8px}.description,.info-card p{line-height:1.7;color:#475569}.room-list{display:grid;gap:14px}.room-item{border:1px solid #e2e8f0;border-radius:12px;padding:16px}.room-selected{border-color:#2563eb;background:#f8fbff}.room-topline{display:flex;justify-content:space-between;gap:12px}.room-topline h3{margin:0 0 5px}.room-topline p{margin:0;color:#64748b;font-size:13px}.room-price{text-align:right;white-space:nowrap}.room-price strong{font-size:18px}.room-price span{display:block;color:#64748b;font-size:12px}.amenity-list{display:flex;gap:7px;flex-wrap:wrap;margin:14px 0}.amenity-pill{padding:5px 9px;border-radius:999px;background:#f1f5f9;color:#334155;font-size:12px}.select-room-btn{margin-top:8px;padding:8px 12px;border:1px solid #2563eb;color:#1d4ed8;background:#fff;border-radius:8px;cursor:pointer;font-weight:700}.booking-card{position:sticky;top:20px}.booking-title{display:flex;align-items:center;justify-content:space-between;gap:10px;padding-bottom:18px;border-bottom:1px solid #e2e8f0}.booking-title h2{margin:4px 0 0;font-size:25px}.booking-title small{font-size:13px;color:#64748b;font-weight:400}.muted{color:#64748b;font-size:13px}.booking-card h3{margin:20px 0}.booking-card form{display:grid;gap:9px}.booking-card label{font-size:13px;font-weight:700;color:#334155;margin-top:5px}.booking-card input,.booking-card select{width:100%;padding:11px 12px;border:1px solid #cbd5e1;border-radius:8px;background:white;color:#0f172a;font:inherit}.price-breakdown{margin-top:10px;padding:13px;background:#f8fafc;border-radius:9px}.price-breakdown div{display:flex;justify-content:space-between;gap:12px;font-size:13px}.price-breakdown small{display:block;margin-top:8px;color:#64748b;line-height:1.5}.primary-btn{border:0;background:#2457c5;color:#fff;padding:12px 16px;border-radius:9px;font-weight:700;cursor:pointer}.primary-btn:disabled{opacity:.6;cursor:not-allowed}.book-btn{width:100%;margin-top:7px}.booking-note{font-size:12px;color:#64748b;line-height:1.5;margin:14px 0 0}.form-message{font-size:13px;line-height:1.5;margin:4px 0}.error-text{color:#b91c1c}.success-text{color:#166534}.state-card{padding:36px;background:#fff;border:1px solid #e2e8f0;border-radius:12px;text-align:center}.error-card{color:#b91c1c}@media(max-width:850px){.content-layout{grid-template-columns:1fr}.booking-card{position:static}.property-heading{align-items:flex-start;flex-direction:column}.gallery-section{grid-template-columns:1fr}.main-photo{height:320px}.thumbnail-grid{grid-template-columns:repeat(3,minmax(0,1fr));max-height:none}.thumbnail{height:100px}}@media(max-width:520px){.details-page{padding:18px 14px 40px}.property-heading h1{font-size:26px}.main-photo{height:250px}.thumbnail-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.info-card,.booking-card{padding:17px}.room-topline{flex-direction:column}.room-price{text-align:left}}
</style>
