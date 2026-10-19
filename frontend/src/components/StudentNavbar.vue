```vue
<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const menuOpen = ref(false)

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<template>
  <nav class="navbar">
    <RouterLink
      to="/student"
      class="logo"
      @click="menuOpen = false"
    >
      Exam<span>Stay</span>
      <small>STUDENT</small>
    </RouterLink>

    <button
      class="menu-toggle"
      @click="menuOpen = !menuOpen"
      aria-label="Toggle navigation"
      :aria-expanded="menuOpen"
    >
      {{ menuOpen ? '✕' : '☰' }}
    </button>

    <div class="nav-links" :class="{ active: menuOpen }">
      <RouterLink
        to="/student"
        class="nav-link"
        @click="menuOpen = false"
      >
        Dashboard
      </RouterLink>

      <RouterLink
        to="/student/bookings"
        class="nav-link"
        @click="menuOpen = false"
      >
        My Bookings
      </RouterLink>

      <RouterLink
        to="/student/profile"
        class="nav-link"
        @click="menuOpen = false"
      >
        Profile
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
  padding: 14px 5%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  background: #0b0b0f;
  border-bottom: 1px solid rgba(212, 175, 113, 0.25);
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.2);
}

.logo {
  display: flex;
  align-items: center;
  gap: 2px;
  color: #fff;
  font-size: 25px;
  font-weight: 800;
  letter-spacing: -0.8px;
  text-decoration: none;
  white-space: nowrap;
}

.logo span {
  color: #d4af71;
}

.logo small {
  margin-left: 9px;
  padding: 5px 7px;
  border: 1px solid rgba(212, 175, 113, 0.4);
  border-radius: 5px;
  color: #d4af71;
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.8px;
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
  color: #d4af71;
  background: rgba(255, 255, 255, 0.06);
}

.nav-link.router-link-exact-active {
  color: #e4c58f;
  background: rgba(212, 175, 113, 0.12);
}

.find-btn {
  padding: 10px 15px;
  border: 1px solid #0f766e;
  border-radius: 8px;
  background: linear-gradient(135deg, #0f766e, #115e59);
  color: #fff;
  font-size: 13px;
  font-weight: 700;
  text-decoration: none;
  white-space: nowrap;
  transition: all 0.25s ease;
}

.find-btn:hover {
  background: #0d9488;
  border-color: #0d9488;
  transform: translateY(-1px);
}

.logout-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  margin-left: 6px;
  padding: 10px 15px;
  border: 1px solid rgba(248, 113, 113, 0.4);
  border-radius: 8px;
  background: rgba(239, 68, 68, 0.1);
  color: #fca5a5;
  font-size: 13px;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
  transition: all 0.25s ease;
}

.logout-btn:hover {
  background: #dc2626;
  border-color: #dc2626;
  color: #fff;
}

.menu-toggle {
  display: none;
  border: none;
  background: transparent;
  color: #fff;
  font-size: 26px;
  cursor: pointer;
}

@media (max-width: 1100px) {
  .navbar {
    flex-wrap: wrap;
  }

  .menu-toggle {
    display: block;
  }

  .nav-links {
    display: none;
    width: 100%;
    padding: 18px 0 8px;
    flex-direction: column;
    align-items: stretch;
    gap: 12px;
  }

  .nav-links.active {
    display: flex;
  }

  .nav-link,
  .find-btn {
    text-align: center;
  }

  .logout-btn {
    justify-content: center;
    margin-left: 0;
  }
}

@media (max-width: 480px) {
  .navbar {
    padding: 14px 4%;
  }

  .logo {
    font-size: 22px;
  }

  .logo small {
    font-size: 8px;
  }
}
</style>
```