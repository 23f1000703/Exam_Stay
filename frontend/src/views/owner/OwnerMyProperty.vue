<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const properties = ref([])
const loading = ref(false)
const error = ref('')

const fetchProperties = async () => {

  loading.value = true
  error.value = ''

  try {

    const response = await fetch(
      'http://127.0.0.1:5000/api/owner/properties',
      {
        method: 'GET',
        headers: {
          'Authentication-Token': authStore.token
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      error.value = data.message || 'Failed to fetch properties.'
      return
    }

    properties.value = data.properties

  } catch (err) {

    console.error(err)
    error.value = 'Unable to connect to server.'

  } finally {

    loading.value = false

  }
}

const viewProperty = (propertyId) => {
  router.push(`/owner/properties/${propertyId}`)
}

const editProperty = (propertyId) => {
  router.push(`/owner/properties/${propertyId}/edit`)
}

const manageImages = (propertyId) => {
  router.push(`/owner/properties/${propertyId}/images`)
}

const deleteProperty = async (propertyId) => {

  const confirmed = confirm(
    'Are you sure you want to delete this property?'
  )

  if (!confirmed) {
    return
  }

  try {

    const response = await fetch(
      `http://127.0.0.1:5000/api/owner/properties/${propertyId}`,
      {
        method: 'DELETE',
        headers: {
          'Authentication-Token': authStore.token
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message || 'Failed to delete property.')
      return
    }

    alert(data.message)

    properties.value = properties.value.filter(
      property => property.id !== propertyId
    )

  } catch (err) {

    console.error(err)
    alert('Unable to connect to server.')

  }
}

onMounted(() => {
  fetchProperties()
})
</script>

<template>

  <div class="page">

    <div class="header">

      <div>
        <h1>My Properties</h1>
        <p>Manage your properties and accommodation details.</p>
      </div>

      <button
        class="add-btn"
        @click="router.push('/owner/properties/add')"
      >
        + Add Property
      </button>

    </div>

    <div
      v-if="loading"
      class="state"
    >
      Loading properties...
    </div>

    <div
      v-else-if="error"
      class="error"
    >
      {{ error }}
    </div>

    <div
      v-else-if="properties.length === 0"
      class="empty"
    >

      <div class="empty-icon">🏠</div>

      <h2>No Properties Yet</h2>

      <p>
        You have not added any property yet.
      </p>

      <button
        class="add-btn"
        @click="router.push('/owner/properties/add')"
      >
        Add Your First Property
      </button>

    </div>

    <div
      v-else
      class="property-grid"
    >

      <div
        v-for="property in properties"
        :key="property.id"
        class="property-card"
      >

        <div class="image-container">

          <img
            v-if="property.primary_image"
            :src="`http://127.0.0.1:5000${property.primary_image}`"
            alt="Property image"
          >

          <div
            v-else
            class="no-image"
          >
            🏠
          </div>

          <span
            class="status"
            :class="property.verification_status"
          >
            {{ property.verification_status }}
          </span>

        </div>

        <div class="property-content">

          <h2>{{ property.name }}</h2>

          <p class="location">
            {{ property.city }}, {{ property.state }}
          </p>

          <p class="address">
            {{ property.address }}
          </p>

          <p
            v-if="property.description"
            class="description"
          >
            {{ property.description }}
          </p>

          <div class="property-info">

            <span>
              🛏 {{ property.total_rooms }} Rooms
            </span>

            <span>
              🖼 {{ property.total_images }} Images
            </span>

          </div>

          <div class="actions">

            <button
              class="view-btn"
              @click="viewProperty(property.id)"
            >
              View
            </button>

            <button
              class="edit-btn"
              @click="editProperty(property.id)"
            >
              Edit
            </button>

            <button
              class="image-btn"
              @click="manageImages(property.id)"
            >
              Images
            </button>

            <button
              class="delete-btn"
              @click="deleteProperty(property.id)"
            >
              Delete
            </button>

          </div>

        </div>

      </div>

    </div>

  </div>

</template>

<style scoped>

.page {
  padding: 32px;
  max-width: 1200px;
  margin: auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.header h1 {
  margin: 0;
  font-size: 30px;
}

.header p {
  margin-top: 8px;
  color: #666;
}

.add-btn {
  border: none;
  background: #f4b400;
  color: #111;
  padding: 12px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}

.add-btn:hover {
  background: #d99d00;
}

.property-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.property-card {
  background: white;
  border-radius: 14px;
  overflow: hidden;
  border: 1px solid #e5e5e5;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.06);
}

.image-container {
  height: 220px;
  position: relative;
  background: #f3f3f3;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.no-image {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 55px;
}

.status {
  position: absolute;
  top: 15px;
  right: 15px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: 600;
  text-transform: capitalize;
}

.status.pending {
  background: #fff3cd;
  color: #856404;
}

.status.approved {
  background: #d4edda;
  color: #155724;
}

.status.rejected {
  background: #f8d7da;
  color: #721c24;
}

.property-content {
  padding: 20px;
}

.property-content h2 {
  margin: 0 0 6px;
  font-size: 21px;
}

.location {
  color: #555;
  font-weight: 600;
  margin: 0 0 8px;
}

.address {
  color: #777;
  margin: 0 0 12px;
}

.description {
  color: #666;
  line-height: 1.5;
}

.property-info {
  display: flex;
  gap: 20px;
  margin: 18px 0;
  color: #555;
  font-size: 14px;
}

.actions {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px;
}

.actions button {
  padding: 10px;
  border-radius: 7px;
  cursor: pointer;
  font-weight: 600;
}

.view-btn {
  border: 1px solid #333;
  background: white;
}

.edit-btn {
  border: 1px solid #f4b400;
  background: #fff8df;
}

.image-btn {
  border: 1px solid #555;
  background: #f5f5f5;
}

.delete-btn {
  border: 1px solid #dc3545;
  background: #fff;
  color: #dc3545;
}

.state {
  text-align: center;
  padding: 80px;
  color: #666;
}

.error {
  padding: 20px;
  background: #ffe5e5;
  color: #b00020;
  border-radius: 8px;
}

.empty {
  text-align: center;
  padding: 80px 20px;
  border: 1px dashed #ccc;
  border-radius: 12px;
}

.empty-icon {
  font-size: 55px;
}

.empty h2 {
  margin-bottom: 8px;
}

.empty p {
  color: #777;
  margin-bottom: 20px;
}

@media (max-width: 800px) {

  .property-grid {
    grid-template-columns: 1fr;
  }

  .header {
    align-items: flex-start;
    gap: 20px;
    flex-direction: column;
  }

}

</style>