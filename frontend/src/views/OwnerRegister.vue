<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const email = ref('')
const password = ref('')
const confirmPassword = ref('')

const name = ref('')
const mobile = ref('')

const idType = ref('')
const idNumber = ref('')

const propertyAddress = ref('')
const perState = ref('')
const perDistrict = ref('')
const perPincode = ref('')

const profilePhoto = ref(null)

const agree = ref(false)

const passwordError = ref('')
const phoneError = ref('')

const validatePassword = () => {
  if (
    password.value.length < 8 ||
    !/[A-Z]/.test(password.value) ||
    !/[a-z]/.test(password.value) ||
    !/[0-9]/.test(password.value) ||
    !/[!@#$]/.test(password.value)
  ) {
    passwordError.value =
      'Password must be at least 8 characters and contain at least one uppercase letter, lowercase letter, number and special character (!@#$).'

    return false
  }

  passwordError.value = ''
  return true
}

const validatePhone = () => {
  const phonePattern = /^[6-9][0-9]{9}$/

  if (!phonePattern.test(mobile.value)) {
    phoneError.value = 'Please enter a valid 10-digit mobile number'
    return false
  }

  phoneError.value = ''
  return true
}

const handlePhoto = (event) => {
  profilePhoto.value = event.target.files[0]
}

const validate = () => {

  if (!email.value || !password.value) {
    alert('Email and Password are required')
    return false
  }

  if (!validatePassword()) {
    alert('Please review your password')
    return false
  }

  if (!validatePhone()) {
    alert('Please enter a valid phone number')
    return false
  }

  if (password.value !== confirmPassword.value) {
    alert('Passwords do not match')
    return false
  }

  if (!name.value) {
    alert('Name is required')
    return false
  }

  if (!idType.value || !idNumber.value) {
    alert('Please fill your identity details')
    return false
  }

  if (
    !propertyAddress.value ||
    !perState.value ||
    !perDistrict.value ||
    !perPincode.value
  ) {
    alert('Please fill all property address details')
    return false
  }

  if (!agree.value) {
    alert('Please accept the terms and conditions')
    return false
  }

  return true
}

const register = async () => {

  if (!validate()) {
    return
  }

  const ownerData = {
    email: email.value,
    password: password.value,
    role: 'owner',

    name: name.value,
    mobile: mobile.value,

    id_type: idType.value,
    id_number: idNumber.value,

    property_address: propertyAddress.value,
    per_state: perState.value,
    per_district: perDistrict.value,
    per_pincode: perPincode.value
  }

  try {

    const response = await fetch(
      'http://localhost:5000/api/ownerregister',
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(ownerData)
      }
    )

    const data = await response.json()

    if (!response.ok) {
      alert(data.message || 'Registration failed')
      return
    }

    console.log(data)

    alert('Owner registration successful')

    router.push('/login')

  } catch (error) {

    console.error(error)

    alert('Unable to connect to server')
  }
}
</script>

<template>
  <div class="register-page">

    <div class="register-container">

      <div class="register-header">
        <h1>Owner Registration</h1>
        <p>Create your ExamStay owner account</p>
      </div>

      <form @submit.prevent="register">

        <div class="section">
          <h2>Account Details</h2>

          <div class="form-group">
            <label>Email</label>
            <input
              v-model="email"
              type="email"
              placeholder="Enter your email"
            >
          </div>

          <div class="form-row">

            <div class="form-group">
              <label>Password</label>

              <input
                v-model="password"
                type="password"
                placeholder="Enter password"
                @input="validatePassword"
              >

              <small v-if="passwordError" class="error">
                {{ passwordError }}
              </small>
            </div>

            <div class="form-group">
              <label>Confirm Password</label>

              <input
                v-model="confirmPassword"
                type="password"
                placeholder="Confirm password"
              >
            </div>

          </div>
        </div>


        <div class="section">

          <h2>Personal Details</h2>

          <div class="form-row">

            <div class="form-group">
              <label>Full Name</label>

              <input
                v-model="name"
                type="text"
                placeholder="Enter full name"
              >
            </div>

            <div class="form-group">
              <label>Mobile Number</label>

              <input
                v-model="mobile"
                type="tel"
                maxlength="10"
                placeholder="10-digit mobile number"
                @input="validatePhone"
              >

              <small v-if="phoneError" class="error">
                {{ phoneError }}
              </small>
            </div>

          </div>

        </div>


        <div class="section">

          <h2>Identity Details</h2>

          <div class="form-row">

            <div class="form-group">

              <label>ID Type</label>

              <select v-model="idType">

                <option value="">
                  Select ID Type
                </option>

                <option value="aadhaar">
                  Aadhaar
                </option>

                <option value="pan">
                  PAN Card
                </option>

                <option value="passport">
                  Passport
                </option>

                <option value="driving_license">
                  Driving License
                </option>

              </select>

            </div>


            <div class="form-group">

              <label>ID Number</label>

              <input
                v-model="idNumber"
                type="text"
                placeholder="Enter ID number"
              >

            </div>

          </div>

        </div>


        <div class="section">

          <h2>Property Address</h2>

          <div class="form-group">

            <label>Property Address</label>

            <textarea
              v-model="propertyAddress"
              placeholder="Enter complete property address"
              rows="4"
            ></textarea>

          </div>


          <div class="form-row">

            <div class="form-group">

              <label>State</label>

              <input
                v-model="perState"
                type="text"
                placeholder="Enter state"
              >

            </div>


            <div class="form-group">

              <label>District</label>

              <input
                v-model="perDistrict"
                type="text"
                placeholder="Enter district"
              >

            </div>

          </div>


          <div class="form-group">

            <label>Pincode</label>

            <input
              v-model="perPincode"
              type="text"
              maxlength="6"
              placeholder="Enter pincode"
            >

          </div>

        </div>


        <div class="section">

          <h2>Profile Photo</h2>

          <div class="form-group">

            <label>Profile Photo</label>

            <input
              type="file"
              accept="image/*"
              @change="handlePhoto"
            >

          </div>

        </div>


        <div class="terms">

          <label>

            <input
              v-model="agree"
              type="checkbox"
            >

            I agree to the terms and conditions

          </label>

        </div>


        <button
          type="submit"
          class="register-btn"
        >
          Create Owner Account
        </button>

      </form>


      <div class="login-link">

        Already have an account?

        <RouterLink to="/login">
          Login
        </RouterLink>

      </div>

    </div>

  </div>
</template>

<style scoped>

.register-page {
  min-height: calc(100vh - 70px);
  padding: 40px 20px;
  background: #f7f7f7;
  box-sizing: border-box;
}

.register-container {
  max-width: 900px;
  margin: 0 auto;
  background: white;
  padding: 40px;
  border-radius: 10px;
  box-shadow: 0 5px 25px rgba(0, 0, 0, 0.08);
}

.register-header {
  text-align: center;
  margin-bottom: 35px;
}

.register-header h1 {
  margin-bottom: 8px;
  font-size: 30px;
  color: #171717;
}

.register-header p {
  margin: 0;
  color: #666;
}

.section {
  margin-bottom: 30px;
  padding-bottom: 25px;
  border-bottom: 1px solid #e5e5e5;
}

.section h2 {
  margin-bottom: 20px;
  font-size: 20px;
  color: #171717;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 18px;
}

.form-group label {
  margin-bottom: 7px;
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 14px;
  box-sizing: border-box;
  width: 100%;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #171717;
}

.form-group textarea {
  resize: vertical;
}

.error {
  margin-top: 5px;
  color: #d32f2f;
  font-size: 12px;
}

.terms {
  margin-bottom: 25px;
  font-size: 14px;
}

.terms input {
  margin-right: 8px;
}

.register-btn {
  width: 100%;
  padding: 14px;
  background: #171717;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
}

.register-btn:hover {
  background: #333;
}

.login-link {
  margin-top: 25px;
  text-align: center;
  font-size: 14px;
  color: #555;
}

.login-link a {
  color: #171717;
  font-weight: 600;
  text-decoration: none;
}

@media (max-width: 700px) {

  .register-container {
    padding: 25px;
  }

  .form-row {
    grid-template-columns: 1fr;
    gap: 0;
  }

}

</style>