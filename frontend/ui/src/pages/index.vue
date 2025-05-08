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
  import axios from 'axios'
  import { useRouter } from 'vue-router'

  const username = ref('')
  const password = ref('')
  const loading = ref(false)
  const showError = ref(false)
  const errorMessage = ref('')
  const router = useRouter()

  const API_URL = 'http://localhost:8000/api/v1/users/login'

  async function login () {
    loading.value = true
    try {
      const res = await axios.post(API_URL, { username: username.value, password: password.value })
      // Store token if needed: localStorage.setItem('token', res.data.access_token)
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
