<template>
  <v-container>
    <v-row class="mb-4">
      <v-col>
        <v-btn color="primary" @click="openCreateDialog">Create User</v-btn>
      </v-col>
    </v-row>
    <v-data-table
      class="elevation-1"
      :headers="headers"
      item-key="id"
      :items="users"
      :loading="loading"
      :search="search"
    >
      <template #top>
        <v-text-field v-model="search" class="mx-4" clearable label="Search" />
      </template>
      <template #item.actions="{ item }">
        <v-btn color="primary" icon="mdi-eye" size="small" @click="openDetailDialog(item)" />
        <v-btn
          color="primary"
          icon="mdi-pencil"
          size="small"
          @click="openEditDialog(item)"
        />
        <v-btn
          color="error"
          icon="mdi-delete"
          size="small"
          @click="openDeleteDialog(item)"
        />
        <v-btn
          v-if="!item.team_member_id || item.team_member_id === 0"
          color="success"
          icon="mdi-plus"
          size="small"
          :title="'Create and assign Team Member'"
          @click="assignTeamMember(item)"
        />
      </template>
    </v-data-table>

    <!-- Edit/Create Dialog -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h6">{{
            dialogMode === "edit" ? "Edit User" : "Create User"
          }}</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="formRef" @submit.prevent="saveUser">
            <v-text-field
              v-model="editedUser.username"
              :autocomplete="dialogMode === 'create' ? 'new-username' : 'current-username'"
              label="Username"
              required
              :rules="[rules.required]"
            />
            <v-text-field
              v-model="editedUser.first_name"
              label="First Name"
              required
              :rules="[rules.required]"
            />
            <v-text-field
              v-model="editedUser.last_name"
              label="Last Name"
              required
              :rules="[rules.required]"
            />
            <v-text-field
              v-model="editedUser.email"
              label="Email"
              required
              :rules="[rules.required, rules.email]"
            />
            <v-switch v-model="editedUser.active" label="Active" />
            <v-text-field
              v-if="dialogMode === 'create' || dialogMode === 'edit'"
              v-model="editedUser.password"
              :append-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
              :autocomplete="dialogMode === 'create' ? 'new-password' : 'current-password'"
              label="Password"
              :required="dialogMode === 'create'"
              :rules="dialogMode === 'create' ? [rules.required] : []"
              :type="showPassword ? 'text' : 'password'"
              @click:append="showPassword = !showPassword"
            />
            <v-select
              v-model="editedUser.team_member_id"
              clearable
              :item-title="tm => `${tm.first_name} ${tm.last_name}${tm.position ? ' (' + tm.position + ')' : ''}`"
              item-value="id"
              :items="allTeamMembers"
              label="Team Member"
            />
            <v-textarea
              v-model="editedUser.note"
              label="Note"
            />
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="closeDialog">Cancel</v-btn>
          <v-btn color="primary" @click="saveUser">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h6">Confirm Delete</v-card-title>
        <v-card-text>Are you sure you want to delete user
          <b>{{ selectedUser?.username }}</b>?</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="error" @click="deleteUser">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Detail Dialog -->
    <v-dialog v-model="detailDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h6">User Details</span>
        </v-card-title>
        <v-card-text>
          <v-list>
            <v-list-item>
              <v-list-item-title>ID</v-list-item-title>
              <v-list-item-subtitle>{{ detailUser?.id }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Username</v-list-item-title>
              <v-list-item-subtitle>{{ detailUser?.username }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>First Name</v-list-item-title>
              <v-list-item-subtitle>{{ detailUser?.first_name }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Last Name</v-list-item-title>
              <v-list-item-subtitle>{{ detailUser?.last_name }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Email</v-list-item-title>
              <v-list-item-subtitle>{{ detailUser?.email }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Active</v-list-item-title>
              <v-list-item-subtitle>{{ detailUser?.active ? 'Yes' : 'No' }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Note</v-list-item-title>
              <v-list-item-subtitle>{{ detailUser?.note }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Team Member ID</v-list-item-title>
              <v-list-item-subtitle>
                {{ detailUser?.team_member_id }}
                <span v-if="detailTeamMember"> ({{ detailTeamMember.first_name }} {{ detailTeamMember.last_name }}<span v-if="detailTeamMember.position">, {{ detailTeamMember.position }}</span>)</span>
              </v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Created At</v-list-item-title>
              <v-list-item-subtitle>{{ detailUser?.created_at }}</v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Updated At</v-list-item-title>
              <v-list-item-subtitle>{{ detailUser?.updated_at }}</v-list-item-subtitle>
            </v-list-item>
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
  import { onMounted, ref } from 'vue';
  import axios from 'axios';

  const users = ref([]);
  const loading = ref(false);
  const search = ref('');
  const dialog = ref(false);
  const deleteDialog = ref(false);
  const detailDialog = ref(false);
  const dialogMode = ref('create'); // 'create' or 'edit'
  const editedUser = ref({
    id: null,
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    note: '',
    active: true,
    team_member_id: null,
  });
  const selectedUser = ref(null);
  const detailUser = ref(null);
  const showPassword = ref(false);
  const formRef = ref(null);
  const detailTeamMember = ref(null);
  const allTeamMembers = ref([]);

  const headers = [
    { title: 'ID', value: 'id' },
    { title: 'Username', value: 'username' },
    { title: 'First Name', value: 'first_name' },
    { title: 'Last Name', value: 'last_name' },
    { title: 'Email', value: 'email' },
    { title: 'Actions', value: 'actions', sortable: false },
  ];

  const rules = {
    required: v => !!v || 'Required',
    email: v => !v || /.+@.+\..+/.test(v) || 'E-mail must be valid',
  };

  const API_URL = 'http://localhost:8000/api/v1/users';

  async function fetchUsers () {
    loading.value = true;
    try {
      const res = await axios.get(API_URL);
      users.value = res.data;
    } finally {
      loading.value = false;
    }
  }

  async function fetchAllTeamMembers () {
    try {
      const res = await axios.get('http://localhost:8000/api/v1/team-members');
      allTeamMembers.value = res.data;
    } catch {
      allTeamMembers.value = [];
    }
  }

  function openCreateDialog () {
    dialogMode.value = 'create';
    editedUser.value = {
      id: null,
      username: '',
      first_name: '',
      last_name: '',
      email: '',
      password: '',
      note: '',
      active: true,
      team_member_id: null,
    };
    dialog.value = true;
  }

  function openEditDialog (user) {
    dialogMode.value = 'edit';
    editedUser.value = {
      id: user.id,
      username: user.username,
      first_name: user.first_name || '',
      last_name: user.last_name || '',
      email: user.email,
      password: '',
      note: user.note || '',
      active: user.active,
      team_member_id: user.team_member_id || null,
    };
    dialog.value = true;
  }

  function closeDialog () {
    dialog.value = false;
  }

  async function saveUser () {
    if (formRef.value && !(await formRef.value.validate())) return;
    if (dialogMode.value === 'create') {
      await axios.post(API_URL, editedUser.value);
    } else {
      const payload = { ...editedUser.value };
      if (!payload.password) delete payload.password;
      await axios.put(`${API_URL}/${editedUser.value.id}`, payload);
    }
    dialog.value = false;
    await fetchUsers();
  }

  function openDeleteDialog (user) {
    selectedUser.value = user;
    deleteDialog.value = true;
  }

  async function deleteUser () {
    await axios.delete(`${API_URL}/${selectedUser.value.id}`);
    deleteDialog.value = false;
    await fetchUsers();
  }

  async function fetchDetailTeamMember (teamMemberId) {
    if (!teamMemberId || teamMemberId === 0) {
      detailTeamMember.value = null;
      return;
    }
    try {
      const res = await axios.get(`http://localhost:8000/api/v1/team-members/${teamMemberId}`);
      detailTeamMember.value = res.data;
    } catch {
      detailTeamMember.value = null;
    }
  }

  function openDetailDialog (user) {
    detailUser.value = user;
    detailDialog.value = true;
    fetchDetailTeamMember(user.team_member_id);
  }

  async function assignTeamMember (user) {
    // Create a new team member with user's first name, last name, email
    const teamMemberPayload = {
      first_name: user.first_name,
      last_name: user.last_name,
      email: user.email,
      phone_number: null,
      position: null,
      notes: 'Autogenerated from user record.',
      supervisor_id: null,
    };
    try {
      const res = await axios.post('http://localhost:8000/api/v1/team-members', teamMemberPayload);
      const newTeamMember = res.data;
      // Update the user with the new team member id
      await axios.put(`${API_URL}/${user.id}`, { team_member_id: newTeamMember.id });
      await fetchUsers();
      await fetchAllTeamMembers();
    } catch {
      alert('Failed to create and assign team member.');
    }
  }

  onMounted(() => {
    fetchUsers();
    fetchAllTeamMembers();
  });
</script>

<style scoped>
.v-data-table {
  background: var(--v-theme-surface);
}
</style>
