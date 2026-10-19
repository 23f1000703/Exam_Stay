<template>
  <div class="register-page">

    <div class="register-card">

      <div class="register-header">
        <p class="label">JOIN EXAMSTAY</p>

        <h1>Create Student Account</h1>

        <p>
          Create your account and find a verified stay for your exam journey.
        </p>
      </div>

      <form @submit.prevent="register">

        <div class="section">
          <h2>Account Details</h2>

          <div class="form-group">
            <label for="email">Email</label>

            <input
              id="email"
              v-model="email"
              type="email"
              placeholder="Enter your email"
              required
            />
          </div>

          <div class="form-row">

            <div class="form-group">
              <label for="password">Password</label>

              <input
                id="password"
                v-model="password"
                type="password"
                placeholder="Create a password"
                required
                @input="validatePassword"
              />

              <div v-if="passwordError" class="error">
                {{ passwordError }}
              </div>
            </div>

            <div class="form-group">
              <label for="confirmPassword">Confirm Password</label>

              <input
                id="confirmPassword"
                v-model="confirmPassword"
                type="password"
                placeholder="Confirm your password"
                required
              />
            </div>

          </div>
        </div>

        <div class="section">
          <h2>Personal Details</h2>

          <div class="form-group">
            <label for="name">Full Name</label>

            <input
              id="name"
              v-model="name"
              type="text"
              placeholder="Enter your full name"
              required
            />
          </div>

          <div class="form-row">

            <div class="form-group">
              <label for="dob">Date of Birth</label>

              <input
                id="dob"
                v-model="dob"
                type="date"
                required
              />
            </div>

            <div class="form-group">
              <label for="gender">Gender</label>

              <select
                id="gender"
                v-model="gender"
                required
              >
                <option value="" disabled>
                  Select gender
                </option>

                <option value="male">
                  Male
                </option>

                <option value="female">
                  Female
                </option>

                <option value="other">
                  Other
                </option>
              </select>
            </div>

          </div>

          <div class="form-group">
            <label for="mobile">Mobile Number</label>

            <input
              id="mobile"
              v-model="mobile"
              type="tel"
              placeholder="Enter your 10-digit mobile number"
              maxlength="10"
              required
              @input="validatePhone"
            />

            <div v-if="phoneError" class="error">
              {{ phoneError }}
            </div>
          </div>

          <div class="form-group">
            <label for="alternateMobile">
              Alternate Mobile Number
            </label>

            <input
              id="alternateMobile"
              v-model="alternateMobile"
              type="tel"
              placeholder="Enter alternate mobile number"
              maxlength="10"
            />
          </div>
        </div>

        <div class="section">
          <h2>Identity Details</h2>

          <div class="form-row">

            <div class="form-group">
              <label for="idType">ID Type</label>

              <select
                id="idType"
                v-model="idType"
                required
              >
                <option value="" disabled>
                  Select ID type
                </option>

                <option value="aadhaar">
                  Aadhaar Card
                </option>

                <option value="passport">
                  Passport
                </option>

                <option value="driving_license">
                  Driving License
                </option>

                <option value="voter_id">
                  Voter ID
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="idNumber">ID Number</label>

              <input
                id="idNumber"
                v-model="idNumber"
                type="text"
                placeholder="Enter ID number"
                required
              />
            </div>

          </div>
        </div>

        <div class="section">
          <h2>Correspondence Address</h2>

          <div class="form-group">
            <label for="corAddress">Address</label>

            <textarea
              id="corAddress"
              v-model="corAddress"
              placeholder="Enter your correspondence address"
              required
            ></textarea>
          </div>

          <div class="form-row">

            <div class="form-group">
              <label for="corState">State</label>

              <input
                id="corState"
                v-model="corState"
                type="text"
                placeholder="Enter state"
                required
              />
            </div>

            <div class="form-group">
              <label for="corDistrict">District</label>

              <input
                id="corDistrict"
                v-model="corDistrict"
                type="text"
                placeholder="Enter district"
                required
              />
            </div>

            <div class="form-group">
              <label for="corPincode">Pincode</label>

              <input
                id="corPincode"
                v-model="corPincode"
                type="text"
                placeholder="Enter pincode"
                maxlength="6"
                required
              />
            </div>

          </div>
        </div>

        <div class="section">

          <div class="section-title">

            <div>
              <h2>Permanent Address</h2>

              <p>
                Enter your permanent address.
              </p>
            </div>

            <label class="same-address">

              <input
                v-model="sameAddress"
                type="checkbox"
                @change="copyAddress"
              />

              Same as correspondence address

            </label>

          </div>

          <div class="form-group">
            <label for="perAddress">Address</label>

            <textarea
              id="perAddress"
              v-model="perAddress"
              placeholder="Enter your permanent address"
            ></textarea>
          </div>

          <div class="form-row">

            <div class="form-group">
              <label for="perState">State</label>

              <input
                id="perState"
                v-model="perState"
                type="text"
                placeholder="Enter state"
                required
              />
            </div>

            <div class="form-group">
              <label for="perDistrict">District</label>

              <input
                id="perDistrict"
                v-model="perDistrict"
                type="text"
                placeholder="Enter district"
                required
              />
            </div>

            <div class="form-group">
              <label for="perPincode">Pincode</label>

              <input
                id="perPincode"
                v-model="perPincode"
                type="text"
                placeholder="Enter pincode"
                maxlength="6"
                required
              />
            </div>

          </div>
        </div>

        <div class="section">
          <h2>Student Details</h2>

          <div class="form-group">
            <label for="studentId">Student ID</label>

            <input
              id="studentId"
              v-model="studentId"
              type="text"
              placeholder="Enter your student ID"
            />
          </div>

          <div class="form-group">
            <label for="collegeName">College Name</label>

            <input
              id="collegeName"
              v-model="collegeName"
              type="text"
              placeholder="Enter your college name"
            />
          </div>

          <div class="form-group">
            <label for="course">Course</label>

            <input
              id="course"
              v-model="course"
              type="text"
              placeholder="Enter your course"
            />
          </div>

          <div class="form-group">
            <label for="profilePhoto">
              Profile Photo
            </label>

            <input
              id="profilePhoto"
              type="file"
              accept="image/*"
              @change="handlePhoto"
            />
          </div>
        </div>

        <div class="terms">

          <label>
            <input
              v-model="agree"
              type="checkbox"
              required
            />

            I agree to the ExamStay terms and conditions.
          </label>

        </div>

        <button type="submit">
          Create Student Account
        </button>

      </form>

      <div class="login-link">

        <p>
          Already have an account?

          <RouterLink to="/login">
            Login
          </RouterLink>
        </p>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const password = ref('')
const confirmPassword = ref('')

const name = ref('')
const dob = ref('')
const gender = ref('')
const mobile = ref('')
const alternateMobile = ref('')

const idType = ref('')
const idNumber = ref('')

const corAddress = ref('')
const corState = ref('')
const corDistrict = ref('')
const corPincode = ref('')

const perAddress = ref('')
const perState = ref('')
const perDistrict = ref('')
const perPincode = ref('')

const studentId = ref('')
const collegeName = ref('')
const course = ref('')
const profilePhoto = ref(null)

const sameAddress = ref(false)
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
    phoneError.value =
      'Please enter a valid 10-digit mobile number'

    return false
  }

  phoneError.value = ''
  return true
}

const copyAddress = () => {
  if (sameAddress.value) {
    perAddress.value = corAddress.value
    perState.value = corState.value
    perDistrict.value = corDistrict.value
    perPincode.value = corPincode.value
  }
}

const handlePhoto = (event) => {
  profilePhoto.value = event.target.files[0]
}

const validate = async () => {

  if (!validatePassword()) {
    alert('Please review your password')
    return false
  }

  if (!validatePhone()) {
    alert('Please enter a valid phone number')
    return false
  }

  if (email.value === '' || password.value === '') {
    alert('Email and Password should not be empty')
    return false
  }

  if (
    name.value === '' ||
    dob.value === '' ||
    gender.value === '' ||
    mobile.value === ''
  ) {
    alert('Please fill all required fields')
    return false
  }

  if (
    idType.value === '' ||
    idNumber.value === ''
  ) {
    alert('Please fill your identity details')
    return false
  }

  if (
    corAddress.value === '' ||
    corState.value === '' ||
    corDistrict.value === '' ||
    corPincode.value === ''
  ) {
    alert('Please fill your correspondence address')
    return false
  }

  if (
    perState.value === '' ||
    perDistrict.value === '' ||
    perPincode.value === ''
  ) {
    alert('Please fill your permanent address')
    return false
  }

  if (password.value !== confirmPassword.value) {
    alert('Passwords do not match')
    return false
  }

  if (!agree.value) {
    alert('Please accept the terms and conditions')
    return false
  }

  return true
}

const register = async () => {

  const isValid = await validate()

  if (!isValid) {
    return
  }

  const studentData = {
    email: email.value,
    password: password.value,
    role: 'customer',

    name: name.value,
    dob: dob.value,
    gender: gender.value,
    mobile: mobile.value,
    alternate_mobile: alternateMobile.value,

    id_type: idType.value,
    id_number: idNumber.value,

    cor_address: corAddress.value,
    cor_state: corState.value,
    cor_district: corDistrict.value,
    cor_pincode: corPincode.value,

    per_address: perAddress.value,
    per_state: perState.value,
    per_district: perDistrict.value,
    per_pincode: perPincode.value,

    student_id: studentId.value,
    college_name: collegeName.value,
    course: course.value
  }

  try {

    const response = await fetch('http://localhost:5000/api/studentregister', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(studentData)
    })

    const data = await response.json()

    if (!response.ok) {
      alert(data.message || 'Registration failed')
      return
    }

    console.log(data)

    alert('Student registration successful')

  } catch (error) {

    console.error(error)

    alert('Unable to connect to server')

  }
}

</script>

<style scoped>
.register-page {
  min-height: calc(100vh - 70px);
  padding: 50px 20px;
  background: #f7f7f5;
}

.register-card {
  width: 100%;
  max-width: 850px;
  margin: auto;
  padding: 45px;
  box-sizing: border-box;
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 10px;
}

.register-header {
  text-align: center;
  margin-bottom: 40px;
}

.label {
  margin-bottom: 12px;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;
  color: #666;
}

.register-header h1 {
  margin: 0 0 12px;
  font-size: 32px;
  color: #171717;
}

.register-header p:last-child {
  margin: 0;
  color: #666;
  line-height: 1.6;
}

.section {
  margin-bottom: 40px;
  padding-bottom: 35px;
  border-bottom: 1px solid #e5e5e5;
}

.section h2 {
  margin: 0 0 22px;
  font-size: 21px;
  color: #171717;
}

.section-title {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 20px;
  margin-bottom: 22px;
}

.section-title h2 {
  margin-bottom: 6px;
}

.section-title p {
  margin: 0;
  color: #777;
  font-size: 14px;
}

.same-address {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: #555;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.form-group label {
  font-size: 14px;
  font-weight: 600;
  color: #333;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  box-sizing: border-box;
  padding: 13px;
  border: 1px solid #ccc;
  border-radius: 6px;
  background: white;
  font-size: 15px;
  outline: none;
  font-family: inherit;
}

.form-group textarea {
  min-height: 100px;
  resize: vertical;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #222;
}

.error {
  color: #c62828;
  font-size: 13px;
  line-height: 1.5;
}

.terms {
  margin-bottom: 25px;
  font-size: 14px;
  color: #555;
}

.terms label {
  display: flex;
  align-items: center;
  gap: 8px;
}

button {
  width: 100%;
  padding: 14px;
  border: none;
  border-radius: 6px;
  background: #171717;
  color: white;
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
}

button:hover {
  opacity: 0.9;
}

.login-link {
  margin-top: 25px;
  text-align: center;
  font-size: 14px;
}

.login-link p {
  color: #666;
}

.login-link a {
  color: #171717;
  font-weight: 600;
  text-decoration: none;
}

@media (max-width: 700px) {
  .register-card {
    padding: 30px 20px;
  }

  .form-row {
    grid-template-columns: 1fr;
    gap: 0;
  }

  .section-title {
    flex-direction: column;
  }

  .register-header h1 {
    font-size: 27px;
  }
}
</style>