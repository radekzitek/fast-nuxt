<template>
  <v-container>
    <v-row class="mb-4">
      <v-col>
        <v-btn color="primary" @click="openCreateDialog">Create Team Member</v-btn>
      </v-col>
    </v-row>
    <v-data-table
      class="elevation-1"
      :headers="headers"
      item-key="id"
      :items="teamMembers"
      :loading="loading"
      :search="search"
    >
      <template #top>
        <v-text-field v-model="search" class="mx-4" clearable label="Search" />
      </template>
      <template #item.actions="{ item }">
        <v-btn color="primary" icon="mdi-eye" size="small" @click="openDetailDialog(item)" />
        <v-btn color="primary" icon="mdi-pencil" size="small" @click="openEditDialog(item)" />
        <v-btn color="error" icon="mdi-delete" size="small" @click="openDeleteDialog(item)" />
        <v-btn
          v-if="!teamMemberUsers[item.id]"
          color="success"
          icon="mdi-plus"
          size="small"
          title="Create user for this team member"
          @click="createUserForTeamMember(item)"
        />
      </template>
    </v-data-table>

    <!-- Edit/Create Dialog -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h6">{{ dialogMode === 'edit' ? 'Edit Team Member' : 'Create Team Member' }}</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="formRef" @submit.prevent="saveTeamMember">
            <v-text-field v-model="editedTeamMember.first_name" label="First Name" required :rules="[rules.required]" />
            <v-text-field v-model="editedTeamMember.last_name" label="Last Name" required :rules="[rules.required]" />
            <v-text-field v-model="editedTeamMember.email" label="Email" required :rules="[rules.required, rules.email]" />
            <v-text-field v-model="editedTeamMember.phone_number" label="Phone Number" />
            <v-text-field v-model="editedTeamMember.position" label="Position" />
            <v-textarea v-model="editedTeamMember.notes" label="Notes" />
            <!-- Supervisor dropdown -->
            <v-select
              v-model="editedTeamMember.supervisor_id"
              clearable
              :item-title="tm => `${tm.first_name} ${tm.last_name}${tm.position ? ' (' + tm.position + ')' : ''}`"
              item-value="id"
              :items="supervisorOptions"
              label="Supervisor"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="closeDialog">Cancel</v-btn>
          <v-btn color="primary" @click="saveTeamMember">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h6">Confirm Delete</v-card-title>
        <v-card-text>Are you sure you want to delete team member <b>{{ selectedTeamMember?.first_name }} {{ selectedTeamMember?.last_name }}</b>?</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="error" @click="deleteTeamMember">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Detail Dialog -->
    <v-dialog v-model="detailDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h6">Team Member Details</span>
        </v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item><v-list-item-title>ID</v-list-item-title><v-list-item-subtitle>{{ detailTeamMember?.id }}</v-list-item-subtitle></v-list-item>
            <v-list-item><v-list-item-title>First Name</v-list-item-title><v-list-item-subtitle>{{ detailTeamMember?.first_name }}</v-list-item-subtitle></v-list-item>
            <v-list-item><v-list-item-title>Last Name</v-list-item-title><v-list-item-subtitle>{{ detailTeamMember?.last_name }}</v-list-item-subtitle></v-list-item>
            <v-list-item><v-list-item-title>Email</v-list-item-title><v-list-item-subtitle>{{ detailTeamMember?.email }}</v-list-item-subtitle></v-list-item>
            <v-list-item><v-list-item-title>Phone Number</v-list-item-title><v-list-item-subtitle>{{ detailTeamMember?.phone_number }}</v-list-item-subtitle></v-list-item>
            <v-list-item><v-list-item-title>Position</v-list-item-title><v-list-item-subtitle>{{ detailTeamMember?.position }}</v-list-item-subtitle></v-list-item>
            <v-list-item><v-list-item-title>Notes</v-list-item-title><v-list-item-subtitle>{{ detailTeamMember?.notes }}</v-list-item-subtitle></v-list-item>
            <v-list-item>
              <v-list-item-title>Supervisor ID</v-list-item-title>
              <v-list-item-subtitle>
                {{ detailTeamMember?.supervisor_id }}
                <span v-if="detailSupervisor"> ({{ detailSupervisor.first_name }} {{ detailSupervisor.last_name }}<span v-if="detailSupervisor.position">, {{ detailSupervisor.position }}</span>)</span>
              </v-list-item-subtitle>
            </v-list-item>
            <v-list-item><v-list-item-title>Created At</v-list-item-title><v-list-item-subtitle>{{ detailTeamMember?.created_at }}</v-list-item-subtitle></v-list-item>
            <v-list-item><v-list-item-title>Updated At</v-list-item-title><v-list-item-subtitle>{{ detailTeamMember?.updated_at }}</v-list-item-subtitle></v-list-item>
          </v-list>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="detailDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-row class="mt-8">
      <v-col cols="12">
        <router-link class="back-icon-link" to="/aiph">
          <v-icon size="32">mdi-arrow-left-circle-outline</v-icon>
          <span>Back to Hub</span>
        </router-link>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
  import { computed, onMounted, ref } from 'vue';
  import api from '@/api';

  const teamMembers = ref([]);
  const teamMemberUsers = ref({}); // Map team_member_id -> user (or null)
  const loading = ref(false);
  const search = ref('');
  const dialog = ref(false);
  const deleteDialog = ref(false);
  const detailDialog = ref(false);
  const dialogMode = ref('create');
  const editedTeamMember = ref({
    id: null,
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    position: '',
    notes: '',
    supervisor_id: null,
  });
  const selectedTeamMember = ref(null);
  const detailTeamMember = ref(null);
  const formRef = ref(null);
  const detailSupervisor = ref(null);

  const headers = [
    { title: 'ID', value: 'id' },
    { title: 'First Name', value: 'first_name' },
    { title: 'Last Name', value: 'last_name' },
    { title: 'Position', value: 'position' },
    { title: 'Phone', value: 'phone_number' },
    { title: 'Actions', value: 'actions', sortable: false },
  ];

  const rules = {
    required: v => !!v || 'Required',
    email: v => !v || /.+@.+\..+/.test(v) || 'E-mail must be valid',
  };

  async function fetchTeamMembers () {
    loading.value = true;
    try {
      const res = await api.get('/team-members');
      teamMembers.value = res.data;
      // For each team member, check if a user exists
      const userChecks = await Promise.all(res.data.map(async tm => {
        try {
          const userRes = await api.get(`/users/by-team-member/${tm.id}`);
          return { id: tm.id, user: userRes.data && userRes.data.length > 0 ? userRes.data[0] : null };
        } catch {
          return { id: tm.id, user: null };
        }
      }));
      teamMemberUsers.value = Object.fromEntries(userChecks.map(u => [u.id, u.user]));
    } finally {
      loading.value = false;
    }
  }

  function removeDiacritics (str) {
    return str.normalize('NFD').replace(/\p{Diacritic}/gu, '');
  }

  async function createUserForTeamMember (teamMember) {
    const username = removeDiacritics((teamMember.first_name[0] + teamMember.last_name).toLowerCase());
    const payload = {
      username,
      first_name: teamMember.first_name,
      last_name: teamMember.last_name,
      email: teamMember.email,
      password: 'default1',
      team_member_id: teamMember.id,
      active: true,
      note: 'Autogenerated from team memeber record.',
    };
    try {
      await api.post('/users', payload);
      await fetchTeamMembers();
    } catch (e) {
      alert('Failed to create user: ' + (e.response?.data?.detail || e.message));
    }
  }

  function openCreateDialog () {
    dialogMode.value = 'create';
    editedTeamMember.value = {
      id: null,
      first_name: '',
      last_name: '',
      email: '',
      phone_number: '',
      position: '',
      notes: '',
      supervisor_id: null,
    };
    dialog.value = true;
  }

  function openEditDialog (member) {
    dialogMode.value = 'edit';
    editedTeamMember.value = { ...member };
    dialog.value = true;
  }

  function closeDialog () {
    dialog.value = false;
  }

  async function saveTeamMember () {
    if (formRef.value && !(await formRef.value.validate())) return;
    if (dialogMode.value === 'create') {
      await api.post('/team-members', editedTeamMember.value);
    } else {
      await api.put(`/team-members/${editedTeamMember.value.id}`, editedTeamMember.value);
    }
    dialog.value = false;
    await fetchTeamMembers();
  }

  function openDeleteDialog (member) {
    selectedTeamMember.value = member;
    deleteDialog.value = true;
  }

  async function deleteTeamMember () {
    // Before deleting, check if any user is assigned to this team member
    try {
      // Fetch users with this team member id
      const usersRes = await api.get('/users', {
        params: { team_member_id: selectedTeamMember.value.id },
      });
      const users = usersRes.data;
      // For each user, set their team_member_id to null
      for (const user of users) {
        if (user.team_member_id === selectedTeamMember.value.id) {
          await api.put(`/users/${user.id}`, { team_member_id: null });
        }
      }
    } catch {
      // Optionally handle error
    }
    // Now delete the team member
    await api.delete(`/team-members/${selectedTeamMember.value.id}`);
    deleteDialog.value = false;
    await fetchTeamMembers();
  }

  async function fetchDetailSupervisor (supervisorId) {
    if (!supervisorId || supervisorId === 0) {
      detailSupervisor.value = null;
      return;
    }
    try {
      const res = await api.get(`/team-members/${supervisorId}`);
      detailSupervisor.value = res.data;
    } catch {
      detailSupervisor.value = null;
    }
  }

  function openDetailDialog (member) {
    detailTeamMember.value = member;
    detailDialog.value = true;
    fetchDetailSupervisor(member.supervisor_id);
  }

  // Computed list of possible supervisors (exclude self)
  const supervisorOptions = computed(() => {
    if (!editedTeamMember.value.id) return teamMembers.value;
    return teamMembers.value.filter(tm => tm.id !== editedTeamMember.value.id);
  });

  onMounted(fetchTeamMembers);
</script>

<style scoped>
.back-icon-link {
  display: flex;
  align-items: center;
  gap: 8px;
  color: inherit;
  text-decoration: none;
  font-weight: 500;
  margin-bottom: 16px;
  transition: color 0.2s;
}
.back-icon-link:hover {
  color: #1976d2;
}
.v-data-table {
  background: var(--v-theme-surface);
}
</style>
