<template>
  <v-app-bar app :color="isDark ? 'primary-darken-4' : 'primary'" :dark="isDark">
    <v-icon class="ml-2" style="cursor:pointer" @click="goToAiph">mdi-crystal-ball</v-icon>
    <v-toolbar-title style="cursor:pointer" @click="goToAiph">AI Performance Hub</v-toolbar-title>
    <v-spacer />

    <!-- User info section - only shown when userData exists -->
    <div v-if="userData" class="mr-4">
      {{ userData.first_name }} {{ userData.last_name }} ({{ userData.username }})
      <v-icon class="ml-2" style="cursor:pointer" @click="showPasswordDialog = true">mdi-key</v-icon>
    </div>

    <!-- Only show logout when userData exists -->
    <v-btn
      v-if="userData"
      icon
      @click="logout"
    >
      <v-icon>mdi-logout</v-icon>
    </v-btn>

    <v-btn icon @click="toggleTheme">
      <v-icon>{{ isDark ? 'mdi-white-balance-sunny' : 'mdi-moon-waning-crescent' }}</v-icon>
    </v-btn>
  </v-app-bar>

  <v-dialog v-model="showPasswordDialog" max-width="400px">
    <v-card>
      <v-card-title>Change Password</v-card-title>
      <v-card-text>
        <v-form ref="passwordFormRef" @submit.prevent="submitPasswordChange">
          <input
            aria-hidden="true"
            autocomplete="username"
            style="display:none"
            tabindex="-1"
            type="text"
            :value="userData?.username"
          >
          <v-text-field
            v-model="currentPassword"
            autocomplete="current-password"
            label="Current Password"
            required
            type="password"
          />
          <v-text-field
            v-model="newPassword"
            autocomplete="new-password"
            label="New Password"
            required
            type="password"
          />
          <v-text-field
            v-model="confirmPassword"
            autocomplete="new-password"
            :error-messages="confirmPassword && newPassword && confirmPassword !== newPassword ? ['Passwords do not match'] : []"
            label="Confirm New Password"
            required
            type="password"
          />
        </v-form>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="showPasswordDialog = false">Cancel</v-btn>
        <v-btn color="primary" @click="submitPasswordChange">Change</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>

  <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="4000">
    {{ snackbarText }}
  </v-snackbar>
</template>

<script setup>
  import { computed, onMounted, ref, watchEffect } from 'vue'
  import { useTheme } from 'vuetify'
  import { useAuthStore } from '@/stores/auth'
  import { useRouter } from 'vue-router'
  import axios from 'axios'

  const theme = useTheme()
  const isDark = computed(() => theme.global.current.value.dark)
  function toggleTheme () {
    theme.global.name.value = isDark.value ? 'light' : 'dark'
  }

  // Store and router
  const auth = useAuthStore()
  const router = useRouter()

  // Local reactive variable for user data
  const userData = ref(null)

  // Fetch user if we have a token but no user data
  function fetchUserIfNeeded () {
    if (auth.token && !auth.user) {
      auth.fetchUser()
    }
  }

  function logout () {
    auth.logout()
    userData.value = null
    router.push('/')
  }

  function goToAiph () {
    router.push('/aiph')
  }

  // Use watchEffect for reactive updates - much more elegant than polling
  watchEffect(() => {
    // This will automatically re-run whenever auth.user changes
    userData.value = auth.user
  })

  // Initial fetch on component mount
  onMounted(() => {
    fetchUserIfNeeded()
  })

  const showPasswordDialog = ref(false)
  const currentPassword = ref('')
  const newPassword = ref('')
  const confirmPassword = ref('')
  const passwordMatchError = ref(false)
  const passwordFormRef = ref(null)

  const snackbar = ref(false)
  const snackbarColor = ref('')
  const snackbarText = ref('')

  async function submitPasswordChange () {
    passwordMatchError.value = false
    if (newPassword.value !== confirmPassword.value) {
      passwordMatchError.value = true
      return
    }
    try {
      await axios.post('http://localhost:8000/api/v1/users/change-password', {
        current_password: currentPassword.value,
        new_password: newPassword.value,
      }, {
        headers: {
          Authorization: `Bearer ${auth.token}`,
        },
      })
      showPasswordDialog.value = false
      currentPassword.value = ''
      newPassword.value = ''
      confirmPassword.value = ''
      snackbarText.value = 'Password changed successfully.'
      snackbarColor.value = 'success'
      snackbar.value = true
    } catch (e) {
      snackbarText.value = 'Failed to change password: ' + (e.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
    }
  }
</script>
