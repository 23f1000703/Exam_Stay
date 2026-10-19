<script setup>
import { reactive, ref } from "vue";
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  name: "",
  description: "",
  address: "",
  city: "",
  district: "",
  state: "",
  pincode: "",
});

const loading = ref(false);
const errorMessage = ref("");
const successMessage = ref("");

async function submitProperty() {
  errorMessage.value = "";
  successMessage.value = "";

  const token = localStorage.getItem("token");

  if (!token) {
    errorMessage.value = "Please login again.";
    return;
  }

  loading.value = true;

  try {
    const response = await fetch(
      "http://127.0.0.1:5000/api/owner/properties",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          'Authentication-Token': authStore.token,
        },
        body: JSON.stringify(form),
      }
    );

    const data = await response.json();
    console.log("Error response:", data)

    if (!response.ok) {
      throw new Error(
        data.message || data.error || "Property not saved."
      );
      
    }

    const propertyId = data.property?.id;

    if (!propertyId) {
      throw new Error("Property ID not available.");
    }

    localStorage.setItem("current_property_id", String(propertyId));

    router.push(`/owner/properties/${propertyId}`);


  } catch (error) {
    errorMessage.value =
      error.message || "Failed to connect to server.";
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="property-form-container">
    <div class="form-card">
      <h2>Add Property</h2>
      <p class="subtitle">Step 1 of 4 — Property Details</p>

      <form @submit.prevent="submitProperty">
        <div class="form-group">
          <label for="name">Property Name *</label>
          <input
            id="name"
            v-model.trim="form.name"
            type="text"
            placeholder="Enter property name"
            required
          />
        </div>

        <div class="form-group">
          <label for="description">Description</label>
          <textarea
            id="description"
            v-model.trim="form.description"
            placeholder="Describe your property"
            rows="4"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="address">Full Address *</label>
          <textarea
            id="address"
            v-model.trim="form.address"
            placeholder="Enter full address"
            rows="3"
            required
          ></textarea>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="city">City *</label>
            <input
              id="city"
              v-model.trim="form.city"
              type="text"
              placeholder="Enter city"
              required
            />
          </div>

          <div class="form-group">
            <label for="district">District *</label>
            <input
              id="district"
              v-model.trim="form.district"
              type="text"
              placeholder="Enter district"
              required
            />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="state">State *</label>
            <input
              id="state"
              v-model.trim="form.state"
              type="text"
              placeholder="Enter state"
              required
            />
          </div>

          <div class="form-group">
            <label for="pincode">Pincode *</label>
            <input
              id="pincode"
              v-model.trim="form.pincode"
              type="text"
              inputmode="numeric"
              pattern="[0-9]{6}"
              maxlength="6"
              placeholder="6-digit pincode"
              required
            />
          </div>
        </div>

        <p v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </p>

        <p v-if="successMessage" class="success-message">
          {{ successMessage }}
        </p>

        <button type="submit" :disabled="loading">
          {{ loading ? "Saving..." : "Save & Continue" }}
        </button>
      </form>
    </div>
  </div>
</template>


<style scoped>
.property-form-container {
  min-height: 100vh;
  padding: 40px 20px;
  background: #f4f6f9;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.form-card {
  width: 100%;
  max-width: 700px;
  padding: 32px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.08);
}

h2 {
  margin: 0 0 8px;
  color: #1f2937;
}

.subtitle {
  margin-bottom: 28px;
  color: #6b7280;
}

.form-group {
  display: flex;
  flex-direction: column;
  flex: 1;
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  gap: 20px;
}

label {
  margin-bottom: 8px;
  font-weight: 600;
  color: #374151;
}

input,
textarea {
  width: 100%;
  box-sizing: border-box;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 7px;
  font: inherit;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.12);
}

textarea {
  resize: vertical;
}

button {
  width: 100%;
  padding: 13px;
  border: none;
  border-radius: 7px;
  background: #2563eb;
  color: white;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.error-message {
  color: #dc2626;
  margin-bottom: 16px;
}

.success-message {
  color: #15803d;
  margin-bottom: 16px;
}

@media (max-width: 600px) {
  .form-card {
    padding: 22px;
  }

  .form-row {
    flex-direction: column;
    gap: 0;
  }
}
</style>
