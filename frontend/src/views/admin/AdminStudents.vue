<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const students = ref([])
const search = ref('')
const loading = ref(true)
const error = ref('')

let searchTimer = null

const fetchStudents = async () => {

  try {

    loading.value = true
    error.value = ''

    const url =
      `http://localhost:5000/api/admin/students?search=${encodeURIComponent(search.value)}`

    const response = await fetch(
      url,
      {
        method: 'GET',
        headers: {
          'Authentication-Token': authStore.token
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(
        data.message || 'Failed to load students'
      )
    }

    students.value = data.students

  } catch (err) {

    console.error(err)

    error.value =
      err.message || 'Unable to load students'

  } finally {

    loading.value = false

  }
}

const handleSearch = () => {

  clearTimeout(searchTimer)

  searchTimer = setTimeout(() => {
    fetchStudents()
  }, 400)

}

const viewStudent = (studentId) => {

  router.push(
    `/admin/students/${studentId}`
  )

}

onMounted(() => {
  fetchStudents()
})
</script>


<template>

  <div class="students-page">

    <div class="page-header">

      <div>
        <p class="label">
          EXAMSTAY ADMIN
        </p>

        <h1>
          Students
        </h1>

        <p class="subtitle">
          View and manage registered students.
        </p>
      </div>

    </div>


    <div class="toolbar">

      <input
        v-model="search"
        @input="handleSearch"
        type="text"
        placeholder="Search by name, email, mobile, college or student ID..."
      />

      <button
        @click="fetchStudents"
        :disabled="loading"
      >
        Refresh
      </button>

    </div>


    <div
      v-if="loading"
      class="state-box"
    >
      Loading students...
    </div>


    <div
      v-else-if="error"
      class="error-box"
    >
      {{ error }}

      <button @click="fetchStudents">
        Try Again
      </button>
    </div>


    <div
      v-else-if="students.length === 0"
      class="state-box"
    >
      No students found.
    </div>


    <div
      v-else
      class="table-wrapper"
    >

      <table>

        <thead>

          <tr>
            <th>#</th>
            <th>Student</th>
            <th>Email</th>
            <th>Mobile</th>
            <th>College</th>
            <th>Course</th>
            <th>Action</th>
          </tr>

        </thead>


        <tbody>

          <tr
            v-for="(student, index) in students"
            :key="student.id"
          >

            <td>
              {{ index + 1 }}
            </td>

            <td>

              <div class="student-name">
                {{ student.name }}
              </div>

              <div class="student-id">
                ID: {{ student.student_id || 'N/A' }}
              </div>

            </td>

            <td>
              {{ student.email }}
            </td>

            <td>
              {{ student.mobile || 'N/A' }}
            </td>

            <td>
              {{ student.college_name || 'N/A' }}
            </td>

            <td>
              {{ student.course || 'N/A' }}
            </td>

            <td>

              <button
                class="view-btn"
                @click="viewStudent(student.id)"
              >
                View Details
              </button>

            </td>

          </tr>

        </tbody>

      </table>

    </div>

  </div>

</template>


<style scoped>

.students-page {
  min-height: calc(100vh - 70px);
  padding: 50px;
  background: #f7f7f5;
}

.page-header {
  margin-bottom: 35px;
}

.label {
  margin: 0 0 10px;

  font-size: 12px;
  font-weight: 700;
  letter-spacing: 2px;

  color: #666;
}

.page-header h1 {
  margin: 0 0 10px;

  font-size: 42px;

  color: #171717;
}

.subtitle {
  margin: 0;

  color: #666;
}


/* Toolbar */

.toolbar {
  display: flex;
  gap: 12px;

  margin-bottom: 25px;
}

.toolbar input {
  flex: 1;

  padding: 13px 15px;

  border: 1px solid #ddd;
  border-radius: 6px;

  background: white;

  outline: none;

  font-size: 14px;
}

.toolbar input:focus {
  border-color: #999;
}

.toolbar button {
  padding: 0 22px;

  border: 1px solid #ccc;
  border-radius: 6px;

  background: white;

  cursor: pointer;

  font-weight: 600;
}


/* Table */

.table-wrapper {
  background: white;

  border: 1px solid #e5e5e5;

  border-radius: 8px;

  overflow-x: auto;
}

table {
  width: 100%;

  border-collapse: collapse;

  min-width: 900px;
}

th {
  padding: 16px;

  text-align: left;

  font-size: 12px;

  letter-spacing: 0.5px;

  color: #666;

  background: #fafafa;

  border-bottom: 1px solid #e5e5e5;
}

td {
  padding: 17px 16px;

  border-bottom: 1px solid #eee;

  font-size: 14px;

  color: #333;
}

tbody tr:hover {
  background: #fafafa;
}

.student-name {
  font-weight: 600;

  color: #171717;
}

.student-id {
  margin-top: 4px;

  font-size: 12px;

  color: #888;
}


/* Button */

.view-btn {
  padding: 8px 13px;

  border: 1px solid #ccc;

  border-radius: 5px;

  background: white;

  cursor: pointer;

  font-size: 13px;

  font-weight: 600;
}

.view-btn:hover {
  border-color: #777;
}


/* States */

.state-box {
  padding: 60px;

  text-align: center;

  background: white;

  border: 1px solid #e5e5e5;

  border-radius: 8px;

  color: #666;
}

.error-box {
  padding: 20px;

  background: white;

  border: 1px solid #e2caca;

  border-radius: 8px;

  color: #8a3333;
}

.error-box button {
  margin-left: 15px;

  padding: 8px 14px;

  border: 1px solid #ccc;

  border-radius: 5px;

  background: white;

  cursor: pointer;
}


@media (max-width: 700px) {

  .students-page {
    padding: 30px 20px;
  }

  .page-header h1 {
    font-size: 34px;
  }

  .toolbar {
    flex-direction: column;
  }

  .toolbar button {
    padding: 12px;
  }

}

</style>