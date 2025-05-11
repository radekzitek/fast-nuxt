<template>
  <v-container>
    <v-row class="mb-4">
      <v-col>
        <v-btn color="primary" @click="openCreateDialog">Create Objective</v-btn>
      </v-col>
    </v-row>
    <v-data-table
      class="elevation-1"
      :headers="headers"
      item-key="id"
      :items="objectives"
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
      </template>
    </v-data-table>

    <ObjectiveEditDialog
      v-model="dialog"
      :objective-id="dialogMode === 'edit' ? editedObjective.id : null"
      @cancel="closeDialog"
      @save="handleSaveObjective"
    />

    <!-- Delete Confirmation Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="text-h6">Confirm Delete</v-card-title>
        <v-card-text>Are you sure you want to delete objective <b>{{ selectedObjective?.title }}</b>?</v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="deleteDialog = false">Cancel</v-btn>
          <v-btn color="error" @click="deleteObjective">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Detail Dialog -->
    <v-dialog v-model="detailDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h6">Objective Details</span>
        </v-card-title>
        <v-card-text>
          <v-row>
            <v-col cols="1">
              <v-list-item-title>ID</v-list-item-title>
              <v-list-item-subtitle>{{ detailObjective?.id }}</v-list-item-subtitle>
            </v-col>
            <v-col cols="11">
              <v-list-item-title>Title</v-list-item-title>
              <v-list-item-subtitle>{{ detailObjective?.title }}</v-list-item-subtitle>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-list-item-title>Description</v-list-item-title>
              <v-list-item-subtitle>{{ detailObjective?.description }}</v-list-item-subtitle>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-list-item-title>Level</v-list-item-title>
              <v-list-item-subtitle>{{ detailObjective?.level }}</v-list-item-subtitle>
            </v-col>
            <v-col>
              <v-list-item-title>Confidentiality</v-list-item-title>
              <v-list-item-subtitle>{{ detailObjective?.confidentiality }}</v-list-item-subtitle>
            </v-col>
            <v-col>
              <v-list-item-title>Strategic Perspective</v-list-item-title>
              <v-list-item-subtitle>{{ detailObjective?.strategic_perspective }}</v-list-item-subtitle>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-list-item-title>Priority</v-list-item-title>
              <v-list-item-subtitle>{{ detailObjective?.priority }}</v-list-item-subtitle>
            </v-col>
            <v-col>
              <v-list-item-title>Status</v-list-item-title>
              <v-list-item-subtitle>{{ detailObjective?.status }}</v-list-item-subtitle>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-list-item-title>Start Date</v-list-item-title>
              <v-list-item-subtitle>{{ detailObjective?.start_date }}</v-list-item-subtitle>
            </v-col>
            <v-col>
              <v-list-item-title>Target Date</v-list-item-title>
              <v-list-item-subtitle>{{ detailObjective?.target_completion_date }}</v-list-item-subtitle>
            </v-col>
          </v-row>
          <v-row>
            <v-col>
              <v-list-item-title>Owner</v-list-item-title>
              <v-list-item-subtitle>{{ getOwnerName(detailObjective?.owner_id) }}</v-list-item-subtitle>
            </v-col>
          </v-row>
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn text @click="detailDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="4000">
      {{ snackbarText }}
    </v-snackbar>
  </v-container>
</template>

<script setup>
  import { onMounted, ref } from 'vue'
  import api from '@/api'
  import ObjectiveEditDialog from '@/components/ObjectiveEditDialog.vue'

  const objectives = ref([])
  const loading = ref(false)
  const search = ref('')
  const dialog = ref(false)
  const deleteDialog = ref(false)
  const detailDialog = ref(false)
  const dialogMode = ref('create')
  const editedObjective = ref({
    id: null,
    title: '',
    description: '',
    priority: '',
    status: '',
    start_date: '',
    target_completion_date: '',
    level: '',
    confidentiality: '',
    strategic_perspective: '',
    owner_id: null,
  })
  const selectedObjective = ref(null)
  const detailObjective = ref(null)

  const headers = [
    { title: 'ID', value: 'id' },
    { title: 'Title', value: 'title' },
    { title: 'Priority', value: 'priority' },
    { title: 'Status', value: 'status' },
    { title: 'Start Date', value: 'start_date' },
    { title: 'Target Date', value: 'target_completion_date' },
    { title: 'Actions', value: 'actions', sortable: false },
  ]

  const enumOptions = ref({
    priority: [],
    status: [],
    level: [],
    confidentiality: [],
    strategic_perspective: [],
  })

  const enumOptionsLoaded = ref(false)

  const teamMembers = ref([])
  const teamMembersLoaded = ref(false)

  const snackbar = ref(false)
  const snackbarColor = ref('')
  const snackbarText = ref('')

  async function fetchEnumOptions () {
    try {
      const res = await api.get('/objectives/enums')
      enumOptions.value = res.data
      enumOptionsLoaded.value = true
    } catch (e) {
      snackbarText.value = 'Failed to load objective options: ' + (e?.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
      enumOptionsLoaded.value = false
    }
  }

  async function fetchTeamMembers () {
    try {
      const res = await api.get('/team-members')
      teamMembers.value = res.data
      teamMembersLoaded.value = true
    } catch (e) {
      snackbarText.value = 'Failed to load team members: ' + (e?.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
      teamMembersLoaded.value = false
    }
  }


  async function fetchObjectives () {
    loading.value = true
    try {
      const res = await api.get('/objectives')
      objectives.value = res.data
    } catch (e) {
      snackbarText.value = 'Failed to load objectives: ' + (e?.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
    } finally {
      loading.value = false
    }
  }

  function openCreateDialog () {
    dialogMode.value = 'create'
    editedObjective.value = {
      id: null,
      title: '',
      description: '',
      priority: '',
      status: '',
      start_date: '',
      target_completion_date: '',
      level: '',
      confidentiality: '',
      strategic_perspective: '',
      owner_id: null,
    }
    dialog.value = true
  }

  function openEditDialog (objective) {
    dialogMode.value = 'edit'
    editedObjective.value = { ...objective }
    delete editedObjective.value.creation_date
    dialog.value = true
  }

  function closeDialog () {
    dialog.value = false
  }

  function handleSaveObjective (obj, formRef) {
    if (formRef && !(formRef.validate && formRef.validate())) return
    saveObjective(obj)
  }

  async function saveObjective (obj) {
    const now = new Date().toISOString()
    const rest = { ...obj }
    const payload = {
      ...rest,
      last_updated_date: now,
    }
    try {
      if (dialogMode.value === 'create') {
        await api.post('/objectives', payload)
        snackbarText.value = 'Objective created successfully.'
        snackbarColor.value = 'success'
      } else {
        await api.put(`/objectives/${editedObjective.value.id}`, payload)
        snackbarText.value = 'Objective updated successfully.'
        snackbarColor.value = 'success'
      }
      snackbar.value = true
      dialog.value = false
      await fetchObjectives()
    } catch (e) {
      snackbarText.value = 'Failed to save objective: ' + (e?.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
    }
  }

  function openDeleteDialog (objective) {
    selectedObjective.value = objective
    deleteDialog.value = true
  }

  async function deleteObjective () {
    try {
      await api.delete(`/objectives/${selectedObjective.value.id}`)
      snackbarText.value = 'Objective deleted.'
      snackbarColor.value = 'success'
      snackbar.value = true
      deleteDialog.value = false
      await fetchObjectives()
    } catch (e) {
      snackbarText.value = 'Failed to delete objective: ' + (e?.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
    }
  }

  function openDetailDialog (objective) {
    detailObjective.value = objective
    detailDialog.value = true
  }

  function getOwnerName (ownerId) {
    const owner = teamMembers.value.find(tm => tm.id === ownerId)
    return owner ? (owner.name || (owner.first_name + ' ' + owner.last_name)) : ownerId
  }

  onMounted(async () => {
    await fetchEnumOptions()
    await fetchTeamMembers()
    await fetchObjectives()
  })
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
