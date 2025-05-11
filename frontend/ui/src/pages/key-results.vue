<template>
  <div class="centered-page">
    <router-link class="back-icon-link" to="/aiph">
      <v-icon size="48">mdi-arrow-left-circle-outline</v-icon>
      <span>Back to Hub</span>
    </router-link>
  </div>
</template>
<script setup>
// Protected by route meta in router
</script>
<style scoped>
.centered-page {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
}
.back-icon-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: inherit;
  text-decoration: none;
  transition: color 0.2s;
}
.back-icon-link:hover {
  color: #1976d2;
}
</style>
