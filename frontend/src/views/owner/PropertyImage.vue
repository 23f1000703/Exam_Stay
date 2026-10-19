<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const property = ref(null)
const selectedImages = ref([])
const imagePreviews = ref([])
const loading = ref(false)
const fetchingProperty = ref(false)
const error = ref('')

const propertyId = route.params.property_id

const fetchProperty = async () => {
  fetchingProperty.value = true
  error.value = ''

  try {
    const response = await fetch(
      `http://127.0.0.1:5000/api/owner/properties/${propertyId}`,
      {
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
    fetchingProperty.value = false
  }
}

const selectImages = (event) => {
  selectedImages.value = Array.from(event.target.files)

  imagePreviews.value = selectedImages.value.map(image =>
    URL.createObjectURL(image)
  )
}

const uploadImages = async () => {
  if (selectedImages.value.length === 0) {
    error.value = 'Please select at least one image.'
    return
  }

  loading.value = true
  error.value = ''

  try {
    const formData = new FormData()

    selectedImages.value.forEach(image => {
      formData.append('images', image)
    })

    const response = await fetch(
      `http://127.0.0.1:5000/api/owner/properties/${propertyId}/images`,
      {
        method: 'POST',
        headers: {
          'Authentication-Token': authStore.token
        },
        body: formData
      }
    )

    const data = await response.json()

    if (!response.ok) {
      error.value = data.error || data.message || 'Failed to upload images.'
      return
    }

    alert(data.message)

    selectedImages.value = []
    imagePreviews.value = []

    router.push('/owner/properties')

  } catch (err) {
    console.error(err)
    error.value = 'Unable to connect to server.'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProperty()
})
</script>

<template>
  <div class="page">

    <div class="header">
      <div>
        <p class="label">OWNER</p>
        <h1>Property Images</h1>
        <p>Add photos of your accommodation.</p>
      </div>

      <button
        class="back-btn"
        @click="router.push('/owner/properties')"
      >
        Back
      </button>
    </div>

    <div v-if="error" class="error">
      {{ error }}
    </div>

    <div v-if="fetchingProperty" class="loading">
      Loading property...
    </div>

    <div v-else-if="property" class="content">

      <section class="property-card">

        <p class="property-label">PROPERTY DETAILS</p>

        <h2>{{ property.name }}</h2>

        <p v-if="property.description" class="description">
          {{ property.description }}
        </p>

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

        <div class="detail">
          <span>Status</span>
          <strong>{{ property.verification_status }}</strong>
        </div>

      </section>

      <section class="upload-card">

        <p class="property-label">PHOTOS</p>

        <h2>Upload Property Photos</h2>

        <label class="upload-area">

          <input
            type="file"
            multiple
            accept=".jpg,.jpeg,.png,.webp"
            @change="selectImages"
          />

          <div class="upload-content">
            <div class="upload-icon">+</div>
            <h3>Select Images</h3>
            <p>JPG, JPEG, PNG or WEBP</p>
          </div>

        </label>

        <div
          v-if="imagePreviews.length"
          class="preview-grid"
        >

          <div
            v-for="(image, index) in imagePreviews"
            :key="index"
            class="preview"
          >
            <img :src="image" />
          </div>

        </div>

        <button
          class="upload-btn"
          :disabled="loading || selectedImages.length === 0"
          @click="uploadImages"
        >
          {{ loading ? 'Uploading...' : 'Upload Images' }}
        </button>

      </section>

    </div>

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
  max-width: 1100px;
  margin: 0 auto 30px;
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
}

.label {
  margin: 0 0 8px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 1.5px;
  color: #6b7280;
}

.header h1 {
  margin: 0;
  font-size: 32px;
  font-weight: 700;
  color: #111827;
}

.header p:last-child {
  margin: 8px 0 0;
  color: #6b7280;
  font-size: 15px;
}

.back-btn {
  padding: 11px 20px;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  background: #ffffff;
  color: #374151;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.back-btn:hover {
  background: #f3f4f6;
}

.error {
  max-width: 1100px;
  margin: 0 auto 20px;
  padding: 14px 16px;
  border: 1px solid #fecaca;
  border-radius: 8px;
  background: #fef2f2;
  color: #b91c1c;
  font-size: 14px;
}

.loading {
  max-width: 1100px;
  margin: 40px auto;
  text-align: center;
  color: #6b7280;
  font-size: 15px;
}

.content {
  max-width: 1100px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 24px;
  align-items: start;
}

.property-card,
.upload-card {
  background: #ffffff;
  border: 1px solid #e5e7eb;
  border-radius: 14px;
  padding: 28px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
}

.property-label {
  margin: 0 0 10px;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.2px;
  color: #6b7280;
}

.property-card h2,
.upload-card h2 {
  margin: 0 0 20px;
  color: #111827;
  font-size: 22px;
  font-weight: 700;
}

.description {
  margin: 0 0 24px;
  color: #6b7280;
  line-height: 1.6;
  font-size: 14px;
}

.detail {
  display: flex;
  justify-content: space-between;
  gap: 20px;
  padding: 14px 0;
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
  max-width: 60%;
  text-align: right;
  color: #374151;
  font-size: 14px;
  font-weight: 600;
  word-break: break-word;
}

.upload-area {
  display: block;
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  background: #fafafa;
  cursor: pointer;
  transition: 0.2s;
}

.upload-area:hover {
  border-color: #9ca3af;
  background: #f9fafb;
}

.upload-area input {
  display: none;
}

.upload-content {
  padding: 45px 20px;
  text-align: center;
}

.upload-icon {
  width: 48px;
  height: 48px;
  margin: 0 auto 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: #111827;
  color: #ffffff;
  font-size: 28px;
  font-weight: 300;
}

.upload-content h3 {
  margin: 0 0 6px;
  color: #111827;
  font-size: 16px;
  font-weight: 600;
}

.upload-content p {
  margin: 0;
  color: #9ca3af;
  font-size: 13px;
}

.preview-grid {
  margin-top: 20px;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}

.preview {
  position: relative;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  border-radius: 10px;
  background: #f3f4f6;
  border: 1px solid #e5e7eb;
}

.preview img {
  width: 100%;
  height: 100%;
  display: block;
  object-fit: cover;
}

.upload-btn {
  width: 100%;
  margin-top: 22px;
  padding: 13px 20px;
  border: none;
  border-radius: 8px;
  background: #111827;
  color: #ffffff;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
}

.upload-btn:hover:not(:disabled) {
  background: #374151;
}

.upload-btn:disabled {
  background: #d1d5db;
  color: #9ca3af;
  cursor: not-allowed;
}

@media (max-width: 850px) {
  .page {
    padding: 25px;
  }

  .content {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 600px) {
  .page {
    padding: 18px;
  }

  .header {
    align-items: flex-start;
  }

  .header h1 {
    font-size: 26px;
  }

  .property-card,
  .upload-card {
    padding: 20px;
  }

  .detail {
    flex-direction: column;
    gap: 5px;
  }

  .detail strong {
    max-width: 100%;
    text-align: left;
  }

  .preview-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>