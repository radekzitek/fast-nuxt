<template>
  <v-container>
    <v-row class="mb-4">
      <v-col />
    </v-row>
    <v-card v-if="objective">
      <v-card-title>
        <span class="text-h6">Objective Dashboard</span>
        <v-btn
          v-if="objective"
          class="ml-3"
          color="primary"
          size="small"
          @click="openEditDialog(objective)"
        >
          <v-icon left size="18">mdi-pencil</v-icon>
          Edit
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-row align="center" class="compact-row" dense no-gutters>
          <v-col class="compact-col" cols="1">
            <div class="field-label">ID</div>
            <div class="field-value">{{ displayFields.ID }}</div>
          </v-col>
          <v-col class="compact-col" cols="5">
            <div class="field-label">Title</div>
            <div class="field-value">{{ displayFields.Title }}</div>
          </v-col>
          <v-col class="compact-col" cols="5">
            <div class="field-label">Owner</div>
            <div class="field-value">
              <template v-if="owner">
                {{ owner.first_name }} {{ owner.last_name }}<span v-if="owner.position"> ({{ owner.position }})</span>
              </template>
            </div>
          </v-col>
        </v-row>
        <v-row align="center" class="compact-row" dense no-gutters>
          <v-col class="compact-col" cols="12">
            <div class="field-label">Description</div>
            <div class="field-value" style="white-space: pre-line;">{{ displayFields.Description }}</div>
          </v-col>
        </v-row>
        <v-row align="center" class="compact-row" dense no-gutters>
          <v-col class="compact-col" cols="12">
            <div class="field-label">Alignment Statement</div>
            <div class="field-value" style="white-space: pre-line;">{{ displayFields['Alignment Statement'] }}</div>
          </v-col>
        </v-row>
        <v-row align="center" class="compact-row" dense no-gutters>
          <v-col class="compact-col" cols="2">
            <div class="field-label">Level</div>
            <div class="field-value">{{ displayFields.Level }}</div>
          </v-col>
          <v-col class="compact-col" cols="2">
            <div class="field-label">Confidentiality</div>
            <div class="field-value">{{ displayFields.Confidentiality }}</div>
          </v-col>
          <v-col class="compact-col" cols="2">
            <div class="field-label">Strategic Perspective</div>
            <div class="field-value">{{ displayFields['Strategic Perspective'] }}</div>
          </v-col>
          <v-col class="compact-col" cols="2">
            <div class="field-label">Priority</div>
            <div class="field-value">{{ displayFields.Priority }}</div>
          </v-col>
          <v-col class="compact-col" cols="2">
            <div class="field-label">Status</div>
            <div class="field-value">{{ displayFields.Status }}</div>
          </v-col>
          <v-col class="compact-col" cols="1">
            <div class="field-label">Review Cadence</div>
            <div class="field-value">{{ displayFields['Review Cadence'] }}</div>
          </v-col>
        </v-row>
        <v-row align="center" class="compact-row" dense no-gutters>
          <v-col class="compact-col" cols="2">
            <div class="field-label">Start Date</div>
            <div class="field-value">{{ displayFields['Start Date'] }}</div>
          </v-col>
          <v-col class="compact-col" cols="2">
            <div class="field-label">Target Date</div>
            <div class="field-value">{{ displayFields['Target Date'] }}</div>
          </v-col>
          <v-col class="compact-col" cols="2">
            <div class="field-label">Last Progress Update</div>
            <div class="field-value">{{ displayFields['Last Review Date'] }}</div>
          </v-col>
        </v-row>
        <v-divider class="my-4" />
        <ProgressAnalysis :key="progressAnalysisKey" :objective-id="objective?.id" />
        <div class="d-flex align-center mb-2">
          <span class="text-h6">Progress Updates</span>
          <v-spacer />
          <v-btn color="primary" size="small" @click="showCreateProgressDialog = true">
            <v-icon left size="18">mdi-plus</v-icon>
            New Progress Update
          </v-btn>
        </div>
        <ProgressUpdateList
          :progress-updates="progressUpdates"
          @delete="openDeleteProgressDialog"
          @edit="openEditProgressDialog"
        />
      </v-card-text>
    </v-card>
    <v-alert v-else type="error">Objective not found.</v-alert>
    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="4000">
      {{ snackbarText }}
    </v-snackbar>
    <v-row class="mt-8">
      <v-col>
        <router-link class="back-icon-link" to="/aiph">
          <v-icon size="32">mdi-arrow-left-circle-outline</v-icon>
          <span>Back to Hub</span>
        </router-link>
      </v-col>
    </v-row>
    <ObjectiveEditDialog
      v-model="showEditDialog"
      :objective-id="editedObjective?.id || null"
      @cancel="onDialogClosed"
      @save="handleSaveObjective"
    />
    <ProgressUpdateEditDialog
      v-model="showCreateProgressDialog"
      :objective-id="objective?.id"
      :progress-update="null"
      @cancel="showCreateProgressDialog = false"
      @save="handleSaveProgressUpdate"
    />
    <ProgressUpdateEditDialog
      v-model="editProgressDialog"
      :objective-id="objective?.id"
      :progress-update="editedProgressUpdate"
      @cancel="editProgressDialog.value = false"
      @save="handleEditProgressUpdate"
    />
    <ProgressUpdateDeleteDialog
      v-model="deleteProgressDialog"
      :progress-update="progressUpdateToDelete"
      @cancel="deleteProgressDialog.value = false"
      @delete="handleDeleteProgressUpdate"
    />
  </v-container>
</template>

<script setup>
  import { computed, onMounted, ref, watch } from 'vue';
  import { useRoute } from 'vue-router';
  import api from '@/api';
  import ObjectiveEditDialog from '@/components/ObjectiveEditDialog.vue';
  import ProgressUpdateEditDialog from '@/components/ProgressUpdateEditDialog.vue';
  import ProgressUpdateList from '@/components/ProgressUpdateList.vue';
  import ProgressUpdateDeleteDialog from '@/components/ProgressUpdateDeleteDialog.vue';
  import ProgressAnalysis from '@/components/ProgressAnalysis.vue';

  defineEmits(['edit-objective']);

  const route = useRoute();
  const objective = ref(null);
  const snackbar = ref(false)
  const snackbarColor = ref('error')
  const snackbarText = ref('')

  const owner = ref(null)

  const showEditDialog = ref(false)
  const editedObjective = ref(null)

  const progressUpdates = ref([])
  const showCreateProgressDialog = ref(false)
  const editProgressDialog = ref(false)
  const editedProgressUpdate = ref(null)

  const deleteProgressDialog = ref(false)
  const progressUpdateToDelete = ref(null)

  const progressAnalysisKey = ref(0)

  function refreshProgressAnalysis () {
    progressAnalysisKey.value++
  }

  function openEditDialog (obj) {
    editedObjective.value = { ...obj };
    showEditDialog.value = true;
  }

  async function handleSaveObjective (obj) {
    showEditDialog.value = false;
    if (obj && obj.id) {
      // Save to backend
      try {
        const now = new Date().toISOString();
        const payload = { ...obj, last_updated_date: now };
        await api.put(`/objectives/${obj.id}`, payload);
        reloadObjective(obj.id);
        snackbarText.value = 'Objective updated successfully.';
        snackbarColor.value = 'success';
        snackbar.value = true;
      } catch (e) {
        snackbarText.value = 'Failed to update objective: ' + (e?.response?.data?.detail || e.message);
        snackbarColor.value = 'error';
        snackbar.value = true;
      }
    }
    refreshProgressAnalysis()
  }

  async function handleSaveProgressUpdate (update) {
    showCreateProgressDialog.value = false;
    if (!update || !update.objective_id) return;
    try {
      await api.post(`/objectives/${update.objective_id}/progress-updates`, update);
      await fetchProgressUpdates();
      // Find the most recent progress update date
      const mostRecent = progressUpdates.value.reduce((max, curr) => {
        return new Date(curr.progress_date) > new Date(max.progress_date) ? curr : max;
      }, progressUpdates.value[0]);
      // Update objective's last_review_date if needed
      if (mostRecent && objective.value) {
        const now = new Date().toISOString();
        const payload = { ...objective.value, last_review_date: mostRecent.progress_date, last_updated_date: now };
        await api.put(`/objectives/${objective.value.id}`, payload);
        await reloadObjective(objective.value.id);
      }
      snackbarText.value = 'Progress update created successfully.';
      snackbarColor.value = 'success';
      snackbar.value = true;
    } catch (e) {
      snackbarText.value = 'Failed to create progress update: ' + (e?.response?.data?.detail || e.message);
      snackbarColor.value = 'error';
      snackbar.value = true;
    }
    refreshProgressAnalysis()
  }

  async function handleEditProgressUpdate (update) {
    editProgressDialog.value = false;
    if (!update || !update.id) return;
    try {
      await api.put(`/objectives/progress-updates/${update.id}`, update);
      await fetchProgressUpdates();
      // Find the most recent progress update date
      const mostRecent = progressUpdates.value.reduce((max, curr) => {
        return new Date(curr.progress_date) > new Date(max.progress_date) ? curr : max;
      }, progressUpdates.value[0]);
      // Update objective's last_review_date if needed
      if (mostRecent && objective.value) {
        const now = new Date().toISOString();
        const payload = { ...objective.value, last_review_date: mostRecent.progress_date, last_updated_date: now };
        await api.put(`/objectives/${objective.value.id}`, payload);
        await reloadObjective(objective.value.id);
      } else {
        await reloadObjective(objective.value.id);
      }
      snackbarText.value = 'Progress update edited successfully.';
      snackbarColor.value = 'success';
      snackbar.value = true;
    } catch (e) {
      snackbarText.value = 'Failed to edit progress update: ' + (e?.response?.data?.detail || e.message);
      snackbarColor.value = 'error';
      snackbar.value = true;
    }
    refreshProgressAnalysis()
  }

  async function handleDeleteProgressUpdate () {
    if (!progressUpdateToDelete.value?.id) return;
    try {
      await api.delete(`/objectives/progress-updates/${progressUpdateToDelete.value.id}`);
      await fetchProgressUpdates();
      // Find the most recent progress update date after deletion
      let mostRecent = null;
      if (progressUpdates.value.length > 0) {
        mostRecent = progressUpdates.value.reduce((max, curr) => {
          return new Date(curr.progress_date) > new Date(max.progress_date) ? curr : max;
        }, progressUpdates.value[0]);
      }
      // Update objective's last_review_date accordingly
      if (objective.value) {
        const now = new Date().toISOString();
        const payload = { ...objective.value, last_review_date: mostRecent ? mostRecent.progress_date : null, last_updated_date: now };
        await api.put(`/objectives/${objective.value.id}`, payload);
        await reloadObjective(objective.value.id);
      } else {
        await reloadObjective(objective.value.id);
      }
      snackbarText.value = 'Progress update deleted.';
      snackbarColor.value = 'success';
      snackbar.value = true;
    } catch (e) {
      snackbarText.value = 'Failed to delete progress update: ' + (e?.response?.data?.detail || e.message);
      snackbarColor.value = 'error';
      snackbar.value = true;
    } finally {
      deleteProgressDialog.value = false;
      progressUpdateToDelete.value = null;
    }
    refreshProgressAnalysis()
  }

  function openEditProgressDialog (update) {
    editedProgressUpdate.value = { ...update }
    editProgressDialog.value = true
  }

  function openDeleteProgressDialog (update) {
    progressUpdateToDelete.value = update
    deleteProgressDialog.value = true
  }

  function onDialogClosed () {
    showEditDialog.value = false;
    if (editedObjective.value && editedObjective.value.id) {
      reloadObjective(editedObjective.value.id);
    }
  }

  function reloadObjective (id) {
    api.get(`/objectives/${id}`).then(res => {
      objective.value = res.data;
      if (res.data && res.data.owner_id) {
        api.get(`/team-members/${res.data.owner_id}`)
          .then(ownerRes => { owner.value = ownerRes.data })
          .catch(() => { owner.value = null });
      }
    });
  }

  async function fetchProgressUpdates () {
    if (!objective.value?.id) return;
    try {
      const res = await api.get(`/objectives/${objective.value.id}/progress-updates`);
      // Sort by progress_date descending
      progressUpdates.value = res.data.sort((a, b) => new Date(b.progress_date) - new Date(a.progress_date));
    } catch (e) {
      progressUpdates.value = [];
      snackbarText.value = e?.response?.data?.detail || e.message || 'Failed to load progress updates.';
      snackbarColor.value = 'error';
      snackbar.value = true;
    }
  }

  const displayFields = computed(() => {
    if (!objective.value) return {};
    const safe = v => (v === undefined || v === null || v === '') ? '-' : v;
    return {
      ID: safe(objective.value.id),
      Title: safe(objective.value.title),
      Description: safe(objective.value.description),
      Priority: safe(objective.value.priority),
      Status: safe(objective.value.status),
      'Start Date': safe(objective.value.start_date),
      'Target Date': safe(objective.value.target_completion_date),
      Level: safe(objective.value.level),
      Confidentiality: safe(objective.value.confidentiality),
      'Strategic Perspective': safe(objective.value.strategic_perspective),
      'Owner ID': safe(objective.value.owner_id),
      'Parent Objective ID': safe(objective.value.parent_objective_id),
      'Review Cadence': safe(objective.value.review_cadence),
      'Last Review Date': safe(objective.value.last_review_date),
      'Alignment Statement': safe(objective.value.alignment_statement),
    };
  });

  onMounted(async () => {
    try {
      const res = await api.get(`/objectives/${route.params.id}`);
      objective.value = res.data;
      if (res.data && res.data.owner_id) {
        try {
          const ownerRes = await api.get(`/team-members/${res.data.owner_id}`)
          owner.value = ownerRes.data
        } catch (e) {
          owner.value = null
          snackbarText.value = e?.response?.data?.detail || e.message || 'Failed to load owner information.'
          snackbarColor.value = 'error'
          snackbar.value = true
        }
      }
    } catch (e) {
      objective.value = null;
      snackbarText.value = e?.response?.data?.detail || e.message || 'Failed to load objective.'
      snackbarColor.value = 'error';
      snackbar.value = true
    }
  });

  watch(objective, fetchProgressUpdates, { immediate: true });
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
.compact-row {
  margin: 0 0 8px 0; /* Add 8px bottom margin for spacing between rows */
  padding: 0;
  flex-wrap: wrap;
}
.compact-col {
  margin: 0 8px 0 0;
  padding: 2px 8px;
  min-width: 120px;
  border-right: 1px solid #eee;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.compact-col:last-child {
  border-right: none;
}
.field-label {
  font-size: 0.8em;
  color: #888;
  margin-bottom: 2px;
}
.field-value {
  font-size: 1em;
  font-weight: 400;
  color: var(--v-theme-on-surface);
}
</style>
