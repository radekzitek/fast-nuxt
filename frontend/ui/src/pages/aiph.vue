<template>
  <div class="aiph-page">
    <div class="icon-row">
      <router-link class="icon-link" to="/team">
        <v-icon size="36">mdi-account-group</v-icon>
        <span>Team</span>
      </router-link>
      <router-link class="icon-link" to="/meetings">
        <v-icon size="36">mdi-calendar-multiselect</v-icon>
        <span>Meetings</span>
      </router-link>
      <router-link class="icon-link" to="/objectives">
        <v-icon size="36">mdi-flag-variant-outline</v-icon>
        <span>Long Term Objectives</span>
      </router-link>
      <router-link class="icon-link" to="/key-results">
        <v-icon size="36">mdi-checkbox-marked-circle-outline</v-icon>
        <span>Key Results</span>
      </router-link>
      <router-link class="icon-link" to="/evaluations">
        <v-icon size="36">mdi-clipboard-check-outline</v-icon>
        <span>Evaluations</span>
      </router-link>
      <router-link class="icon-link" to="/users">
        <v-icon size="36">mdi-account-outline</v-icon>
        <span>Users</span>
      </router-link>
    </div>
    <div class="aiph-content">
      <div v-if="loading" class="loading">Loading dashboard...</div>
      <template v-else>
        <TeamTree v-if="teamMembers.length && userTeamMemberId" :members="teamMembers" :user-team-member-id="userTeamMemberId" />
        <div v-else class="no-team">No team data available.</div>
      </template>
    </div>
  </div>
</template>

<script setup>
  import { onMounted, ref } from 'vue';
  import TeamTree from '@/components/TeamTree.vue';
  import api from '@/api';

  const teamMembers = ref([]);
  const userTeamMemberId = ref(null); // This should be set to the logged-in user's team_member id
  const loading = ref(true);

  onMounted(async () => {
    try {
      // Fetch all team members
      const teamRes = await api.get('/team-members');
      teamMembers.value = teamRes.data;
      // Fetch the logged-in user's team_member id (token is included automatically)
      const userRes = await api.get('/users/me');
      userTeamMemberId.value = userRes.data.team_member_id;
      console.log('User Team Member ID:', userTeamMemberId.value);
    } catch (e) {
      // Handle error
      console.error(e);
    } finally {
      loading.value = false;
    }
  });
</script>

<style scoped>
.aiph-page {
  padding: 2rem;
}
.icon-row {
  display: flex;
  justify-content: space-evenly;
  gap: 2rem;
  margin-bottom: 2rem;
  align-items: center;
}
.icon-link {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-decoration: none;
  color: inherit;
  transition: color 0.2s;
}
.icon-link:hover {
  color: #1976d2;
}
</style>
