<template>
  <v-app-bar app :color="isDark ? 'primary-darken-4' : 'primary'" :dark="isDark">
    <v-icon class="ml-2">mdi-crystal-ball</v-icon>
    <v-toolbar-title>AI Performance Hub</v-toolbar-title>
    <v-spacer />

    <!-- User info section - only shown when userData exists -->
    <div v-if="userData" class="mr-4">
      {{ userData.first_name }} {{ userData.last_name }} ({{ userData.username }})
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
</template>

<script setup>
  import { computed, onMounted, ref, watchEffect } from 'vue'
  import { useTheme } from 'vuetify'
  import { useAuthStore } from '@/stores/auth'
  import { useRouter } from 'vue-router'

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

  // Use watchEffect for reactive updates - much more elegant than polling
  watchEffect(() => {
    // This will automatically re-run whenever auth.user changes
    userData.value = auth.user
  })

  // Initial fetch on component mount
  onMounted(() => {
    fetchUserIfNeeded()
  })
</script>
