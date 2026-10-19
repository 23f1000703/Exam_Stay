<script setup>
import { useAuthStore } from './stores/auth'

import PublicNavbar from './components/PublicNavbar.vue'
import StudentNavbar from './components/StudentNavbar.vue'
import OwnerNavbar from './components/OwnerNavbar.vue'
import AdminNavbar from './components/AdminNavbar.vue'

const authStore = useAuthStore()
</script>

<template>
  <AdminNavbar v-if="authStore.role === 'admin'" />

  <StudentNavbar v-else-if="authStore.role === 'customer'" />

  <OwnerNavbar v-else-if="authStore.role === 'owner'" />

  <PublicNavbar v-else />

  <main>
    <RouterView />
  </main>
</template>

<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Arial, sans-serif;
}

main {
  min-height: calc(100vh - 70px);
}
</style>