<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" class="fill-height" justify="center">
      <v-col cols="12" md="4" sm="8">
        <v-card>
          <v-card-title class="text-h6">Login</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="login">
              <v-text-field
                v-model="username"
                autocomplete="username"
                label="Username"
                required
              />
              <v-text-field
                v-model="password"
                autocomplete="current-password"
                label="Password"
                required
                type="password"
              />
              <v-btn block color="primary" :loading="loading" type="submit">Login</v-btn>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-snackbar v-model="showError" color="error" timeout="4000">
      {{ errorMessage }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
  import { ref } from 'vue'

  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/auth'
  import api from '@/api'

  const username = ref('')
  const password = ref('')
  const loading = ref(false)
  const showError = ref(false)
  const errorMessage = ref('')
  const router = useRouter()
  const auth = useAuthStore()

  async function login () {
    loading.value = true
    try {
      const params = new URLSearchParams()
      params.append('username', username.value)
      params.append('password', password.value)
      const res = await api.post('/users/token', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      })
      auth.setToken(res.data.access_token)
      auth.setRefreshToken(res.data.refresh_token)
      await auth.fetchUser()
      router.push('/aiph')
    } catch (err) {
      errorMessage.value = err?.response?.data?.detail || 'Login failed'
      showError.value = true
    } finally {
      loading.value = false
    }
  }
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}
</style>
