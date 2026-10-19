<script setup>
import { reactive, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../../stores/auth";

const router = useRouter();
const authStore = useAuthStore();

const API = "http://127.0.0.1:5000/api";

const form = reactive({
  room_number: "",
  room_type: "",
  capacity: 1,
  price_per_night: "",
  available: true,
});

const amenities = ref([]);
const selectedAmenities = ref([]);
const customAmenity = ref("");

const loading = ref(false);
const loadingAmenities = ref(false);
const addingAmenity = ref(false);

const errorMessage = ref("");
const successMessage = ref("");

const propertyId = localStorage.getItem("current_property_id");

function getHeaders() {
  const token = authStore.token || localStorage.getItem("token");

  return {
    "Authentication-Token": token,
  };
}

// Fetch available amenities
async function fetchAmenities() {
  const token = authStore.token || localStorage.getItem("token");

  if (!token) {
    errorMessage.value = "Login token nahi mila. Please dobara login karo.";
    return;
  }

  loadingAmenities.value = true;

  try {
    const response = await fetch(`${API}/amenities`, {
      method: "GET",
      headers: getHeaders(),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.message || "Amenities load nahi ho payi."
      );
    }

    amenities.value = data.amenities || [];
  } catch (error) {
    errorMessage.value =
      error.message || "Amenities load karne mein problem hui.";
  } finally {
    loadingAmenities.value = false;
  }
}

// Add a custom amenity
async function addCustomAmenity() {
  errorMessage.value = "";
  successMessage.value = "";

  const name = customAmenity.value.trim();

  if (!name) {
    errorMessage.value = "Amenity ka naam enter karo.";
    return;
  }

  const token = authStore.token || localStorage.getItem("token");

  if (!token) {
    errorMessage.value = "Login token nahi mila. Please dobara login karo.";
    return;
  }

  addingAmenity.value = true;

  try {
    const response = await fetch(`${API}/amenities`, {
      method: "POST",
      headers: {
        ...getHeaders(),
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ name }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.message || "Nayi amenity add nahi ho payi."
      );
    }

    const newAmenity = data.amenity;

    if (!newAmenity || !newAmenity.id) {
      throw new Error("Server se amenity ki valid ID nahi mili.");
    }

    const existing = amenities.value.find(
      (item) => Number(item.id) === Number(newAmenity.id)
    );

    if (!existing) {
      amenities.value.push(newAmenity);
      amenities.value.sort((a, b) =>
        a.name.localeCompare(b.name)
      );
    }

    // Automatically select the added amenity
    if (
      !selectedAmenities.value.includes(Number(newAmenity.id))
    ) {
      selectedAmenities.value.push(Number(newAmenity.id));
    }

    customAmenity.value = "";
    successMessage.value = `"${newAmenity.name}" amenity select ho gayi.`;
  } catch (error) {
    errorMessage.value =
      error.message || "Nayi amenity add nahi ho payi.";
  } finally {
    addingAmenity.value = false;
  }
}

// Save room
async function submitRoom() {
  errorMessage.value = "";
  successMessage.value = "";

  if (!propertyId) {
    errorMessage.value =
      "Property ID nahi mili. Pehle Step 1 mein property save karo.";
    return;
  }

  const token = authStore.token || localStorage.getItem("token");

  if (!token) {
    errorMessage.value = "Login token nahi mila. Please dobara login karo.";
    return;
  }

  if (!form.room_number.trim()) {
    errorMessage.value = "Room number enter karo.";
    return;
  }

  if (!form.room_type) {
    errorMessage.value = "Room type select karo.";
    return;
  }

  if (
    !Number.isInteger(Number(form.capacity)) ||
    Number(form.capacity) < 1
  ) {
    errorMessage.value =
      "Capacity kam se kam 1 aur whole number honi chahiye.";
    return;
  }

  if (
    form.price_per_night === "" ||
    !Number.isFinite(Number(form.price_per_night)) ||
    Number(form.price_per_night) < 0
  ) {
    errorMessage.value = "Valid price enter karo. Price negative nahi ho sakta.";
    return;
  }

  loading.value = true;

  try {
    const response = await fetch(
      `${API}/owner/properties/${propertyId}/rooms`,
      {
        method: "POST",
        headers: {
          ...getHeaders(),
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          room_number: form.room_number.trim(),
          room_type: form.room_type,
          capacity: Number(form.capacity),
          price_per_night: Number(form.price_per_night),
          available: form.available,

          // Amenities are saved with the room
          amenities: selectedAmenities.value.map(Number),
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      throw new Error(
        data.message || data.error || "Room save nahi ho paya."
      );
    }

    successMessage.value = "Room successfully add ho gaya!";

    console.log("Saved Room:", data.room);

    // Reset form
    form.room_number = "";
    form.room_type = "";
    form.capacity = 1;
    form.price_per_night = "";
    form.available = true;

    selectedAmenities.value = [];
    customAmenity.value = "";
  } catch (error) {
    errorMessage.value =
      error.message || "Server se connect nahi ho paya.";
  } finally {
    loading.value = false;
  }
}

onMounted(fetchAmenities);
</script>

<template>
  <div class="room-form-container">
    <div class="form-card">
      <h2>Add Room Details</h2>
      <p class="subtitle">Step 2 of 4 — Room Details</p>

      <form @submit.prevent="submitRoom">
        <!-- Room Number -->
        <div class="form-group">
          <label for="room_number">Room Number *</label>

          <input
            id="room_number"
            v-model.trim="form.room_number"
            type="text"
            placeholder="Example: 101"
            required
          />
        </div>

        <!-- Room Type -->
        <div class="form-group">
          <label for="room_type">Room Type *</label>

          <select
            id="room_type"
            v-model="form.room_type"
            required
          >
            <option value="" disabled>Select room type</option>
            <option value="Single">Single</option>
            <option value="Double">Double Sharing</option>
            <option value="Triple">Triple Sharing</option>
            <option value="Dormitory">Dormitory</option>
          </select>
        </div>

        <!-- Capacity and Price -->
        <div class="form-row">
          <div class="form-group">
            <label for="capacity">Capacity *</label>

            <input
              id="capacity"
              v-model.number="form.capacity"
              type="number"
              min="1"
              step="1"
              required
            />
          </div>

          <div class="form-group">
            <label for="price_per_night">Price Per Night (₹) *</label>

            <input
              id="price_per_night"
              v-model="form.price_per_night"
              type="number"
              min="0"
              step="0.01"
              placeholder="Enter price"
              required
            />
          </div>
        </div>

        <!-- Availability -->
        <div class="form-group checkbox-group">
          <input
            id="available"
            v-model="form.available"
            type="checkbox"
          />

          <label for="available">
            Room is currently available
          </label>
        </div>

        <!-- Amenities -->
        <div class="form-group amenities-section">
          <label>Room Amenities</label>

          <p class="help-text">
            Is room mein available amenities select karo.
          </p>

          <p v-if="loadingAmenities" class="help-text">
            Amenities load ho rahi hain...
          </p>

          <div
            v-else-if="amenities.length"
            class="amenities-grid"
          >
            <label
              v-for="amenity in amenities"
              :key="amenity.id"
              class="amenity-option"
            >
              <input
                v-model="selectedAmenities"
                type="checkbox"
                :value="Number(amenity.id)"
              />

              <span>{{ amenity.name }}</span>
            </label>
          </div>

          <p v-else class="help-text">
            Abhi koi amenity available nahi hai.
          </p>

          <div class="custom-amenity">
            <label for="custom_amenity">
              Add a new amenity
            </label>

            <div class="custom-amenity-row">
              <input
                id="custom_amenity"
                v-model.trim="customAmenity"
                type="text"
                placeholder="Example: Air Conditioning"
                @keyup.enter.prevent="addCustomAmenity"
              />

              <button
                type="button"
                class="add-amenity-button"
                :disabled="addingAmenity || !customAmenity.trim()"
                @click="addCustomAmenity"
              >
                {{ addingAmenity ? "Adding..." : "Add" }}
              </button>
            </div>
          </div>
        </div>

        <!-- Messages -->
        <p v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </p>

        <p v-if="successMessage" class="success-message">
          {{ successMessage }}
        </p>

        <!-- Save -->
        <button type="submit" :disabled="loading">
          {{ loading ? "Saving..." : "Save Room" }}
        </button>

        <!-- Back -->
        <button
          type="button"
          class="back-button"
          @click="router.back()"
        >
          Back
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.room-form-container {
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
select {
  width: 100%;
  box-sizing: border-box;
  padding: 12px;
  border: 1px solid #d1d5db;
  border-radius: 7px;
  font: inherit;
  background: white;
}

input:focus,
select:focus {
  outline: none;
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.12);
}

.checkbox-group {
  flex-direction: row;
  align-items: center;
  gap: 10px;
}

.checkbox-group input {
  width: auto;
}

.checkbox-group label {
  margin: 0;
}

.amenities-section {
  padding: 18px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #f9fafb;
}

.help-text {
  margin: 0 0 14px;
  color: #6b7280;
  font-size: 14px;
  font-weight: 400;
}

.amenities-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 20px;
}

.amenity-option {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 0;
  padding: 11px;
  border: 1px solid #e5e7eb;
  border-radius: 7px;
  background: white;
  font-weight: 400;
  cursor: pointer;
}

.amenity-option input {
  width: auto;
  margin: 0;
  accent-color: #2563eb;
}

.custom-amenity {
  margin-top: 8px;
}

.custom-amenity-row {
  display: flex;
  align-items: stretch;
  gap: 10px;
}

.custom-amenity-row input {
  flex: 1;
  min-width: 0;
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
  margin-bottom: 12px;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.custom-amenity-row .add-amenity-button {
  width: auto;
  min-width: 90px;
  margin-bottom: 0;
}

.back-button {
  background: #e5e7eb;
  color: #374151;
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

  .amenities-grid {
    grid-template-columns: 1fr;
  }
}
</style>