<template>
  <v-app-bar app :color="isDark ? 'primary-darken-4' : 'primary'" :dark="isDark">
    <v-toolbar-title>Fast-Nuxt User Admin</v-toolbar-title>
    <v-spacer />
    <v-btn icon @click="toggleTheme">
      <v-icon>{{ isDark ? 'mdi-white-balance-sunny' : 'mdi-moon-waning-crescent' }}</v-icon>
    </v-btn>
  </v-app-bar>
</template>

<script setup>
  import { computed } from 'vue'
  import { useTheme } from 'vuetify'

  const theme = useTheme()
  const isDark = computed(() => theme.global.current.value.dark)
  function toggleTheme () {
    theme.global.name.value = isDark.value ? 'light' : 'dark'
  }
</script>
