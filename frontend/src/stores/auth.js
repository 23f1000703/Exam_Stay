
import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', () => {
    const role = ref(localStorage.getItem('role'))
    const token = ref(localStorage.getItem('auth_token'))
    const userId = ref(localStorage.getItem('userId'))

    const isLoggedIn = computed(() => Boolean(token.value))

    function login(authToken, userRole, id) {
        token.value = authToken
        role.value = userRole
        userId.value = id

        localStorage.setItem('auth_token', authToken)
        localStorage.setItem('role', userRole)
        localStorage.setItem('userId', id)

        console.log('Token saved:', Boolean(token.value))
        console.log('Role:', role.value)
    }

    function logout() {
        token.value = null
        role.value = null
        userId.value = null

        localStorage.removeItem('auth_token')
        localStorage.removeItem('role')
        localStorage.removeItem('userId')
    }

    return {
        role,
        token,
        userId,
        isLoggedIn,
        login,
        logout
    }
})
