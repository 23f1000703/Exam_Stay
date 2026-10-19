<script setup>
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <nav class="navbar">
    <RouterLink to="/admin" class="logo">
      ExamStay<span> Admin</span>
      <small>CONTROL PANEL</small>
    </RouterLink>

    <div class="nav-links">
      <RouterLink to="/admin" class="nav-link">
        Dashboard
      </RouterLink>

      <RouterLink to="/admin/students" class="nav-link">
        Users
      </RouterLink>

      <RouterLink to="/admin/properties" class="nav-link">
        Properties
      </RouterLink>

      <RouterLink to="/admin/bookings" class="nav-link">
        Bookings
      </RouterLink>

      <RouterLink to="/admin/verifications" class="nav-link">
        Verifications
      </RouterLink>

      <button @click="logout" class="logout-btn">
        Logout <span>↗</span>
      </button>
    </div>
  </nav>
</template>

<style scoped>
.navbar {
  min-height: 76px;
  padding: 16px 5%;
  background: #0b0b0f;
  border-bottom: 1px solid rgba(212, 175, 113, 0.25);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 28px;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.18);
}

.logo {
  display: flex;
  align-items: center;
  gap: 5px;
  color: #f8fafc;
  text-decoration: none;
  font-size: 23px;
  font-weight: 800;
  letter-spacing: -0.7px;
  white-space: nowrap;
}

.logo span {
  color: #d4af71;
}

.logo small {
  margin-left: 8px;
  padding: 5px 7px;
  border: 1px solid rgba(212, 175, 113, 0.4);
  border-radius: 5px;
  color: #d4af71;
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 1px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-link {
  padding: 10px 12px;
  border-radius: 8px;
  color: #cbd5e1;
  font-size: 13px;
  font-weight: 500;
  text-decoration: none;
  white-space: nowrap;
  transition: all 0.25s ease;
}

.nav-link:hover {
  background: rgba(255, 255, 255, 0.06);
  color: #d4af71;
}

.nav-link.router-link-exact-active {
  background: rgba(212, 175, 113, 0.12);
  color: #e4c58f;
}

.logout-btn {
  margin-left: 8px;
  padding: 10px 16px;
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(248, 113, 113, 0.4);
  border-radius: 8px;
  color: #fca5a5;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.25s ease;
  white-space: nowrap;
}

.logout-btn:hover {
  background: #dc2626;
  border-color: #dc2626;
  color: #ffffff;
  transform: translateY(-1px);
}

.logout-btn span {
  font-size: 16px;
}

@media (max-width: 1100px) {
  .navbar {
    align-items: flex-start;
    flex-direction: column;
    gap: 16px;
  }

  .nav-links {
    width: 100%;
    flex-wrap: wrap;
  }
}

@media (max-width: 600px) {
  .navbar {
    padding: 16px 4%;
  }

  .logo {
    font-size: 20px;
    flex-wrap: wrap;
  }

  .logo small {
    font-size: 8px;
  }

  .nav-links {
    gap: 6px;
  }

  .nav-link {
    padding: 9px 10px;
    font-size: 12px;
  }

  .logout-btn {
    margin-left: 0;
  }
}
</style>
