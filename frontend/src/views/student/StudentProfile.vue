<template>
  <div class="profile-page">
    <header class="page-header">
      <div>
        <h1>My Profile</h1>
        <p>Manage your photo and personal information.</p>
      </div>
      <RouterLink to="/student" class="back-btn">
        Back to Dashboard
      </RouterLink>
    </header>

    <div v-if="loading" class="message">Loading profile...</div>

    <div v-else-if="loadError" class="alert error">
      {{ loadError }}
      <button type="button" @click="fetchProfile">Try Again</button>
    </div>

    <form v-else @submit.prevent="saveProfile" class="profile-form">
      <div v-if="successMessage" class="alert success">
        {{ successMessage }}
      </div>
      <div v-if="errorMessage" class="alert error">
        {{ errorMessage }}
      </div>

      <!-- Profile Photo -->
      <section class="photo-section">
        <div class="photo-preview">
          <img
            v-if="photoPreview"
            :src="photoPreview"
            alt="Student profile photo"
            class="profile-image"
          />
          <div v-else class="photo-placeholder">
            {{ profile.name ? profile.name.charAt(0).toUpperCase() : 'S' }}
          </div>
        </div>

        <div class="photo-controls">
          <h2>Profile Photo</h2>
          <p>Choose a JPG, PNG or WEBP image. Maximum size: 5 MB.</p>

          <div class="photo-buttons">
            <label for="photo-upload" class="upload-btn">
              {{ photoFile ? 'Choose Another Photo' : 'Upload / Change Photo' }}
            </label>
            <input
              id="photo-upload"
              type="file"
              accept="image/jpeg,image/png,image/webp"
              @change="handlePhotoChange"
              hidden
            />

            <button
              v-if="photoPreview"
              type="button"
              class="remove-btn"
              @click="removePhoto"
            >
              Remove Photo
            </button>
          </div>

          <p v-if="photoFile" class="selected-file">
            Selected: {{ photoFile.name }}
          </p>
        </div>
      </section>

      <section class="form-section">
        <h2>Personal Information</h2>
        <div class="form-grid">
          <div class="field">
            <label for="name">Full Name *</label>
            <input id="name" v-model="profile.name" required maxlength="120" />
          </div>

          <div class="field">
            <label for="dob">Date of Birth</label>
            <input id="dob" v-model="profile.dob" type="date" />
          </div>

          <div class="field">
            <label for="gender">Gender</label>
            <select id="gender" v-model="profile.gender">
              <option value="">Select gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div class="field">
            <label for="mobile">Mobile Number *</label>
            <input id="mobile" v-model="profile.mobile" required maxlength="20" />
          </div>

          <div class="field">
            <label for="alternate_mobile">Alternate Mobile</label>
            <input
              id="alternate_mobile"
              v-model="profile.alternate_mobile"
              maxlength="20"
            />
          </div>

          <div class="field">
            <label for="id_type">ID Type</label>
            <select id="id_type" v-model="profile.id_type">
              <option value="">Select ID type</option>
              <option value="Aadhaar">Aadhaar</option>
              <option value="PAN">PAN Card</option>
              <option value="Passport">Passport</option>
              <option value="Voter ID">Voter ID</option>
              <option value="Other">Other</option>
            </select>
          </div>

          <div class="field">
            <label for="id_number">ID Number</label>
            <input id="id_number" v-model="profile.id_number" maxlength="100" />
          </div>

          <div class="field">
            <label for="student_id">Student ID</label>
            <input id="student_id" v-model="profile.student_id" maxlength="100" />
          </div>
        </div>
      </section>

      <section class="form-section">
        <h2>Correspondence Address</h2>
        <div class="form-grid">
          <div class="field full-width">
            <label for="cor_address">Address</label>
            <textarea id="cor_address" v-model="profile.cor_address" rows="3" />
          </div>
          <div class="field">
            <label for="cor_state">State</label>
            <input id="cor_state" v-model="profile.cor_state" />
          </div>
          <div class="field">
            <label for="cor_district">District</label>
            <input id="cor_district" v-model="profile.cor_district" />
          </div>
          <div class="field">
            <label for="cor_pincode">PIN Code</label>
            <input id="cor_pincode" v-model="profile.cor_pincode" maxlength="10" />
          </div>
        </div>
      </section>

      <section class="form-section">
        <h2>Permanent Address</h2>
        <div class="form-grid">
          <div class="field full-width">
            <label for="per_address">Address</label>
            <textarea id="per_address" v-model="profile.per_address" rows="3" />
          </div>
          <div class="field">
            <label for="per_state">State</label>
            <input id="per_state" v-model="profile.per_state" />
          </div>
          <div class="field">
            <label for="per_district">District</label>
            <input id="per_district" v-model="profile.per_district" />
          </div>
          <div class="field">
            <label for="per_pincode">PIN Code</label>
            <input id="per_pincode" v-model="profile.per_pincode" maxlength="10" />
          </div>
        </div>
      </section>

      <section class="form-section">
        <h2>College Information</h2>
        <div class="form-grid">
          <div class="field">
            <label for="college_name">College Name</label>
            <input id="college_name" v-model="profile.college_name" />
          </div>
          <div class="field">
            <label for="course">Course</label>
            <input id="course" v-model="profile.course" />
          </div>
        </div>
      </section>

      <div class="form-actions">
        <button
          type="button"
          class="cancel-btn"
          @click="fetchProfile"
          :disabled="saving"
        >
          Discard Changes
        </button>
        <button type="submit" class="save-btn" :disabled="saving">
          {{ saving ? 'Saving...' : 'Save Changes' }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted, onBeforeUnmount } from 'vue'
import { RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const API_URL = 'http://localhost:5000/api/student/profile'
const SERVER_URL = 'http://localhost:5000'

const loading = ref(true)
const saving = ref(false)
const loadError = ref('')
const errorMessage = ref('')
const successMessage = ref('')

const photoFile = ref(null)
const photoPreviewUrl = ref('')
const savedPhoto = ref('')
const photoRemoved = ref(false)

const emptyProfile = () => ({
  name: '',
  dob: '',
  gender: '',
  mobile: '',
  alternate_mobile: '',
  id_type: '',
  id_number: '',
  cor_address: '',
  cor_state: '',
  cor_district: '',
  cor_pincode: '',
  per_address: '',
  per_state: '',
  per_district: '',
  per_pincode: '',
  student_id: '',
  college_name: '',
  course: ''
})

const profile = reactive(emptyProfile())

const photoPreview = computed(() => {
  if (photoPreviewUrl.value) return photoPreviewUrl.value
  if (photoRemoved.value) return ''
  if (!savedPhoto.value) return ''

  if (/^https?:\/\//i.test(savedPhoto.value)) {
    return savedPhoto.value
  }

  return `${SERVER_URL}/${savedPhoto.value.replace(/^\/+/, '')}`
})

const clearPreviewUrl = () => {
  if (photoPreviewUrl.value) {
    URL.revokeObjectURL(photoPreviewUrl.value)
    photoPreviewUrl.value = ''
  }
}

const handlePhotoChange = (event) => {
  const file = event.target.files?.[0]
  event.target.value = ''

  if (!file) return

  const allowedTypes = ['image/jpeg', 'image/png', 'image/webp']

  if (!allowedTypes.includes(file.type)) {
    errorMessage.value = 'Please select a JPG, PNG or WEBP image.'
    return
  }

  if (file.size > 5 * 1024 * 1024) {
    errorMessage.value = 'Photo size must be 5 MB or less.'
    return
  }

  clearPreviewUrl()
  photoFile.value = file
  photoRemoved.value = false
  photoPreviewUrl.value = URL.createObjectURL(file)
  errorMessage.value = ''
  successMessage.value = ''
}

const removePhoto = () => {
  clearPreviewUrl()
  photoFile.value = null
  photoRemoved.value = true
  savedPhoto.value = ''
  errorMessage.value = ''
}

const setProfile = (data) => {
  Object.assign(profile, emptyProfile(), data)
  savedPhoto.value = data.profile_photo || ''
  photoFile.value = null
  photoRemoved.value = false
  clearPreviewUrl()
}

const fetchProfile = async () => {
  loading.value = true
  loadError.value = ''
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const response = await fetch(API_URL, {
      headers: {
        'Authentication-Token': authStore.token
      }
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Unable to load profile.')
    }

    setProfile(data.profile)
  } catch (error) {
    console.error('Fetch profile error:', error)
    loadError.value = error.message || 'Unable to load profile.'
  } finally {
    loading.value = false
  }
}

const saveProfile = async () => {
  saving.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const formData = new FormData()

    Object.entries(profile).forEach(([key, value]) => {
      formData.append(key, value ?? '')
    })

    if (photoFile.value) {
      formData.append('profile_photo', photoFile.value)
    }

    formData.append('remove_photo', photoRemoved.value ? 'true' : 'false')

    const response = await fetch(API_URL, {
      method: 'PUT',
      headers: {
        'Authentication-Token': authStore.token
      },
      body: formData
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || 'Unable to update profile.')
    }

    setProfile(data.profile)
    successMessage.value = data.message || 'Profile updated successfully.'
  } catch (error) {
    console.error('Update profile error:', error)
    errorMessage.value = error.message || 'Unable to update profile.'
  } finally {
    saving.value = false
  }
}

onMounted(fetchProfile)
onBeforeUnmount(clearPreviewUrl)
</script>

<style scoped>
.profile-page {
  min-height: 100vh;
  padding: 32px;
  background: #f5f7fb;
  color: #1e293b;
}

.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 24px;
}

.page-header h1 {
  margin: 0 0 8px;
  font-size: 28px;
}

.page-header p {
  margin: 0;
  color: #64748b;
}

.back-btn {
  padding: 10px 15px;
  color: #334155;
  background: white;
  border: 1px solid #dbe2ea;
  border-radius: 8px;
  text-decoration: none;
  white-space: nowrap;
}

.profile-form {
  max-width: 1000px;
  margin: 0 auto;
  padding: 26px;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
}

.photo-section {
  display: flex;
  align-items: center;
  gap: 24px;
  padding-bottom: 26px;
  margin-bottom: 26px;
  border-bottom: 1px solid #e2e8f0;
}

.photo-preview {
  width: 120px;
  height: 120px;
  flex-shrink: 0;
  overflow: hidden;
  border: 3px solid #e2e8f0;
  border-radius: 50%;
  background: #eff6ff;
}

.profile-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-placeholder {
  width: 100%;
  height: 100%;
  display: grid;
  place-items: center;
  color: #1d4ed8;
  font-size: 42px;
  font-weight: 700;
}

.photo-controls h2 {
  margin: 0 0 8px;
  font-size: 19px;
}

.photo-controls p {
  color: #64748b;
  font-size: 13px;
}

.photo-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 12px;
}

.upload-btn,
.remove-btn {
  display: inline-block;
  padding: 10px 14px;
  border: none;
  border-radius: 8px;
  font: inherit;
  font-size: 13px;
  font-weight: 650;
  cursor: pointer;
}

.upload-btn {
  background: #2563eb;
  color: white;
}

.remove-btn {
  background: #fee2e2;
  color: #991b1b;
}

.selected-file {
  overflow-wrap: anywhere;
}

.form-section {
  padding-bottom: 24px;
  margin-bottom: 24px;
  border-bottom: 1px solid #e2e8f0;
}

.form-section h2 {
  margin: 0 0 20px;
  font-size: 19px;
}

.form-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.full-width {
  grid-column: 1 / -1;
}

.field label {
  color: #475569;
  font-size: 13px;
  font-weight: 650;
}

.field input,
.field select,
.field textarea {
  width: 100%;
  box-sizing: border-box;
  padding: 11px 12px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: white;
  color: #1e293b;
  font: inherit;
  font-size: 14px;
}

.field input:focus,
.field select:focus,
.field textarea:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 2px #dbeafe;
}

.field textarea {
  resize: vertical;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.save-btn,
.cancel-btn {
  padding: 12px 18px;
  border: none;
  border-radius: 8px;
  font-weight: 650;
  cursor: pointer;
}

.save-btn {
  background: #2563eb;
  color: white;
}

.cancel-btn {
  background: #e2e8f0;
  color: #334155;
}

.save-btn:disabled,
.cancel-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.alert,
.message {
  padding: 14px;
  margin-bottom: 20px;
  border-radius: 8px;
}

.success {
  background: #dcfce7;
  color: #166534;
}

.error {
  background: #fee2e2;
  color: #991b1b;
}

@media (max-width: 650px) {
  .profile-page {
    padding: 16px;
  }

  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .profile-form {
    padding: 18px;
  }

  .photo-section {
    align-items: flex-start;
    flex-direction: column;
  }

  .form-grid {
    grid-template-columns: 1fr;
  }

  .full-width {
    grid-column: auto;
  }

  .form-actions {
    flex-direction: column-reverse;
  }

  .form-actions button {
    width: 100%;
  }
}
</style>
