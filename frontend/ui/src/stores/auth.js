import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')
  const refreshToken = ref(localStorage.getItem('refresh_token') || '')

  function setToken (newToken) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  function setRefreshToken (newRefreshToken) {
    refreshToken.value = newRefreshToken
    localStorage.setItem('refresh_token', newRefreshToken)
  }

  function setUser (userInfo) {
    user.value = userInfo
  }

  async function fetchUser () {
    if (!token.value) return
    try {
      const res = await axios.get('http://localhost:8000/api/v1/users/me', {
        headers: { Authorization: `Bearer ${token.value}` },
      })
      setUser(res.data)
    } catch (e) {
      setUser(null)
      console.error('Failed to fetch user', e)
    }
  }

  function logout () {
    token.value = ''
    refreshToken.value = ''
    user.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('refresh_token')
  }

  return { user, token, refreshToken, setToken, setRefreshToken, setUser, fetchUser, logout }
})
