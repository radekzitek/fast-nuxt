import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('token') || '')

  function setToken (newToken) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  function setUser (userInfo) {
    user.value = userInfo
  }

  async function fetchUser () {
    if (!token.value) return
    try {
      console.log('Fetching user with token:', token.value)
      const res = await axios.get('http://localhost:8000/api/v1/users/me', {
        headers: { Authorization: `Bearer ${token.value}` },
      })
      setUser(res.data)
      console.log('User fetched:', res.data)
    } catch (e) {
      setUser(null)
      console.error('Failed to fetch user', e)
    }
  }

  function logout () {
    token.value = ''
    user.value = null
    localStorage.removeItem('token')
  }

  return { user, token, setToken, setUser, fetchUser, logout }
})
