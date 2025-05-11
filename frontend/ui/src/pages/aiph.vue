<template>
  <div class="aiph-page">
    <div class="icon-row">
      <div class="team-icon-group">
        <router-link class="icon-link" to="/team">
          <v-icon size="36">mdi-account-group</v-icon>
          <span>Team</span>
        </router-link>
        <v-btn class="mt-2" color="primary" size="small" @click="openCreateTeamMemberDialog">Create Team Member</v-btn>
      </div>
      <router-link class="icon-link" to="/meetings">
        <v-icon size="36">mdi-calendar-multiselect</v-icon>
        <span>Meetings</span>
      </router-link>
      <div class="objectives-icon-group">
        <router-link class="icon-link" to="/objectives">
          <v-icon size="36">mdi-flag-variant-outline</v-icon>
          <span>Long Term Objectives</span>
        </router-link>
        <v-btn class="mt-2" color="primary" size="small" @click="openCreateDialog">Create Objective</v-btn>
      </div>
      <router-link class="icon-link" to="/key-results">
        <v-icon size="36">mdi-checkbox-marked-circle-outline</v-icon>
        <span>Key Results</span>
      </router-link>
      <router-link class="icon-link" to="/evaluations">
        <v-icon size="36">mdi-clipboard-check-outline</v-icon>
        <span>Evaluations</span>
      </router-link>
      <div class="users-icon-group">
        <router-link class="icon-link" to="/users">
          <v-icon size="36">mdi-account-outline</v-icon>
          <span>Users</span>
        </router-link>
        <v-btn class="mt-2" color="primary" size="small" @click="openCreateUserDialog">Create User</v-btn>
      </div>
    </div>
    <div class="aiph-content">
      <div v-if="loading" class="loading">Loading dashboard...</div>
      <template v-else>
        <TeamTree
          v-if="teamMembers.length && userTeamMemberId"
          :members="teamMembers"
          :user-team-member-id="userTeamMemberId"
          @edit-objective="handleEditObjective"
          @edit-team-member="handleEditTeamMember"
        />
        <div v-else class="no-team">No team data available.</div>
      </template>
    </div>
    <ObjectiveEditDialog
      v-model="showObjectiveDialog"
      :objective-id="dialogMode === 'edit' ? editedObjective.id : null"
      @cancel="() => { showObjectiveDialog = false }"
      @save="handleSaveObjective"
    />
    <TeamMemberEditDialog
      v-model="showTeamMemberDialog"
      :team-member-id="teamMemberDialogId"
      @cancel="() => { showTeamMemberDialog = false }"
      @save="handleSaveTeamMember"
    />
    <UserEditDialog
      v-model="showUserDialog"
      :user-id="userDialogId"
      @cancel="() => { showUserDialog = false }"
      @save="handleSaveUser"
    />
    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="4000">
      {{ snackbarText }}
    </v-snackbar>
  </div>
</template>

<script setup>
  import { onMounted, ref } from 'vue';
  import TeamTree from '@/components/TeamTree.vue';
  import ObjectiveEditDialog from '@/components/ObjectiveEditDialog.vue';
  import TeamMemberEditDialog from '@/components/TeamMemberEditDialog.vue';
  import UserEditDialog from '@/components/UserEditDialog.vue';
  import api from '@/api';

  const teamMembers = ref([]);
  const userTeamMemberId = ref(null); // This should be set to the logged-in user's team_member id
  const loading = ref(true);
  const snackbar = ref(false);
  const snackbarColor = ref('');
  const snackbarText = ref('');

  const showObjectiveDialog = ref(false);
  const dialogMode = ref('edit');
  const editedObjective = ref({});
  const enumOptions = ref({ priority: [], status: [], level: [], confidentiality: [], strategic_perspective: [] });
  const enumOptionsLoaded = ref(false);
  const teamMembersLoaded = ref(false);

  const showTeamMemberDialog = ref(false);
  const teamMemberDialogId = ref(null);

  const showUserDialog = ref(false);
  const userDialogId = ref(null);

  async function fetchEnumOptions () {
    try {
      const res = await api.get('/objectives/enums');
      enumOptions.value = res.data;
      enumOptionsLoaded.value = true;
    } catch (e) {
      snackbarText.value = 'Failed to load objective options: ' + (e?.response?.data?.detail || e.message);
      snackbarColor.value = 'error';
      snackbar.value = true;
      enumOptionsLoaded.value = false;
    }
  }

  async function fetchTeamMembers () {
    try {
      const res = await api.get('/team-members');
      teamMembers.value = res.data;
      teamMembersLoaded.value = true;
    } catch (e) {
      snackbarText.value = 'Failed to load team members: ' + (e?.response?.data?.detail || e.message);
      snackbarColor.value = 'error';
      snackbar.value = true;
      teamMembersLoaded.value = false;
    }
  }

  function handleEditObjective (obj) {
    dialogMode.value = 'edit';
    editedObjective.value = { ...obj };
    showObjectiveDialog.value = true;
  }

  function handleSaveObjective (obj, formRef) {
    if (formRef && !(formRef.validate && formRef.validate())) return;
    saveObjective(obj);
  }

  async function saveObjective (obj) {
    const now = new Date().toISOString();
    const rest = { ...obj };
    const payload = {
      ...rest,
      last_updated_date: now,
    };
    try {
      await api.put(`/objectives/${obj.id}`, payload);
      snackbarText.value = 'Objective updated successfully.';
      snackbarColor.value = 'success';
      snackbar.value = true;
      showObjectiveDialog.value = false;
      // Reload dashboard data after editing objective
      await reloadDashboard();
    } catch (e) {
      snackbarText.value = 'Failed to save objective: ' + (e?.response?.data?.detail || e.message);
      snackbarColor.value = 'error';
      snackbar.value = true;
    }
  }

  async function reloadDashboard () {
    loading.value = true;
    try {
      const teamRes = await api.get('/team-members');
      teamMembers.value = teamRes.data;
      const userRes = await api.get('/users/me');
      userTeamMemberId.value = userRes.data.team_member_id;
    } catch (e) {
      snackbarText.value = 'Failed to reload dashboard data: ' + (e?.response?.data?.detail || e.message);
      snackbarColor.value = 'error';
      snackbar.value = true;
    } finally {
      loading.value = false;
    }
  }

  function openCreateDialog () {
    dialogMode.value = 'create';
    editedObjective.value = { id: null };
    showObjectiveDialog.value = true;
  }

  function openCreateTeamMemberDialog () {
    teamMemberDialogId.value = null;
    showTeamMemberDialog.value = true;
  }

  function openCreateUserDialog () {
    userDialogId.value = null;
    showUserDialog.value = true;
  }

  async function handleSaveTeamMember (teamMember, formRef) {
    if (formRef && formRef.validate && !formRef.validate()) return;
    try {
      if (teamMember.id) {
        await api.put(`/team-members/${teamMember.id}`, teamMember);
        snackbarText.value = 'Team member updated successfully.';
      } else {
        await api.post('/team-members', teamMember);
        snackbarText.value = 'Team member created successfully.';
      }
      snackbarColor.value = 'success';
      snackbar.value = true;
      showTeamMemberDialog.value = false;
      await fetchTeamMembers();
    } catch (e) {
      snackbarText.value = 'Failed to save team member: ' + (e?.response?.data?.detail || e.message);
      snackbarColor.value = 'error';
      snackbar.value = true;
    }
  }

  async function handleSaveUser (user, formRef) {
    if (formRef && formRef.validate && !formRef.validate()) return
    try {
      await api.post('/users', user)
      snackbarText.value = 'User created successfully.'
      snackbarColor.value = 'success'
      snackbar.value = true
      showUserDialog.value = false
      // await fetchUsers()
    } catch (e) {
      snackbarText.value = 'Failed to create user: ' + (e?.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
    }
  }

  function handleEditTeamMember (member) {
    teamMemberDialogId.value = member.id;
    showTeamMemberDialog.value = true;
  }

  onMounted(async () => {
    loading.value = true;
    await fetchEnumOptions();
    await fetchTeamMembers();
    try {
      // Fetch all team members
      const teamRes = await api.get('/team-members');
      teamMembers.value = teamRes.data;
      // Fetch the logged-in user's team_member id (token is included automatically)
      const userRes = await api.get('/users/me');
      userTeamMemberId.value = userRes.data.team_member_id;
      // console.log('User Team Member ID:', userTeamMemberId.value);
    } catch (e) {
      snackbarText.value = 'Failed to load dashboard data: ' + (e?.response?.data?.detail || e.message);
      snackbarColor.value = 'error';
      snackbar.value = true;
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
.objectives-icon-group {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.team-icon-group {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.users-icon-group {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
