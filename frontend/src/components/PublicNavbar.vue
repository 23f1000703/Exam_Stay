```vue
<template>
  <nav class="navbar">
    <div class="navbar-container">
      <RouterLink to="/" class="brand">
        Stay<span>Ease</span>
      </RouterLink>

      <button
        class="menu-toggle"
        @click="menuOpen = !menuOpen"
        aria-label="Toggle navigation"
      >
        ☰
      </button>

      <div class="nav-links" :class="{ active: menuOpen }">
        <RouterLink to="/" @click="menuOpen = false">
          Home
        </RouterLink>

        <RouterLink to="/login" @click="menuOpen = false">
          Login
        </RouterLink>

        <RouterLink
          to="/register"
          class="student-btn"
          @click="menuOpen = false"
        >
          Register as Student
        </RouterLink>

        <RouterLink
          to="/ownerregister"
          class="owner-btn"
          @click="menuOpen = false"
        >
          Register as Owner
        </RouterLink>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";

const menuOpen = ref(false);
</script>


<style scoped>
.navbar {
  background: #0b0b0f;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding: 17px 5%;
  position: sticky;
  top: 0;
  z-index: 1000;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}

.navbar-container {
  max-width: 1200px;
  margin: auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 20px;
}

.brand {
  color: #ffffff;
  font-size: 26px;
  font-weight: 800;
  letter-spacing: -0.8px;
  text-decoration: none;
}

.brand span {
  color: #d4af71;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 25px;
}

.nav-links a {
  color: #d1d5db;
  font-size: 14px;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.25s ease;
}

.nav-links a:hover,
.nav-links a.router-link-exact-active {
  color: #d4af71;
}

.nav-links .student-btn,
.nav-links .owner-btn {
  padding: 11px 17px;
  border-radius: 9px;
  font-weight: 600;
  transition: all 0.25s ease;
}

/* Student: Elegant teal */
.nav-links .student-btn {
  background: #0f766e;
  color: #ffffff;
  border: 1px solid #0f766e;
  box-shadow: 0 4px 12px rgba(15, 118, 110, 0.18);
}

.nav-links .student-btn:hover {
  background: #115e59;
  border-color: #115e59;
  color: #ffffff;
  transform: translateY(-2px);
}

/* Owner: Gold accent */
.nav-links .owner-btn {
  background: linear-gradient(135deg, #d4af71, #b88a44);
  color: #111111;
  border: 1px solid #d4af71;
  box-shadow: 0 4px 12px rgba(212, 175, 113, 0.15);
}

.nav-links .owner-btn:hover {
  background: linear-gradient(135deg, #e5c58f, #d4af71);
  color: #111111;
  transform: translateY(-2px);
}

.menu-toggle {
  display: none;
  color: #ffffff;
  background: transparent;
  border: none;
  font-size: 27px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .navbar {
    padding: 15px 5%;
  }

  .brand {
    font-size: 23px;
  }

  .menu-toggle {
    display: block;
  }

  .nav-links {
    display: none;
    position: absolute;
    top: 100%;
    left: 0;
    right: 0;
    padding: 22px;
    background: #0b0b0f;
    border-bottom: 1px solid rgba(255, 255, 255, 0.12);
    flex-direction: column;
    align-items: stretch;
    gap: 20px;
  }

  .nav-links.active {
    display: flex;
  }

  .nav-links a {
    text-align: center;
  }

  .nav-links .student-btn,
  .nav-links .owner-btn {
    text-align: center;
    padding: 12px 16px;
  }
}
</style>
