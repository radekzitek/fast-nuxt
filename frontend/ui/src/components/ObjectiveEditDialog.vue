<template>
  <v-dialog v-model="dialogVisible" max-width="600px">
    <v-card>
      <v-card-title class="py-2 px-3">
        <span class="text-h6">Edit Objective</span>
      </v-card-title>
      <v-card-text class="py-2 px-3">
        <v-form ref="formRef" @submit.prevent="onSave">
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-text-field
                v-model="localObjective.title"
                density="compact"
                hide-details
                label="Title"
                required
                :rules="[rules.required]"
              />
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1" cols="11">
              <v-textarea v-model="localObjective.description" density="compact" hide-details label="Description" />
            </v-col>
            <v-col class="d-flex align-center py-1 px-1" cols="1">
              <v-btn
                class="ml-1"
                :disabled="rewritingDescription"
                icon
                :loading="rewritingDescription"
                size="small"
                title="Rewrite Description with AI"
                @click="rewriteDescription"
              >
                <v-icon>mdi-robot</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1" cols="11">
              <v-textarea
                v-model="localObjective.alignment_statement"
                auto-grow
                density="compact"
                hide-details
                label="Alignment Statement"
                style="white-space: pre-line;"
              />
            </v-col>
            <v-col class="d-flex align-center py-1 px-1" cols="1">
              <v-btn
                class="ml-1"
                :disabled="rewritingAlignmentStatement"
                icon
                :loading="rewritingAlignmentStatement"
                size="small"
                title="Rewrite Alignment Statement with AI"
                @click="rewriteAlignmentStatement"
              >
                <v-icon>mdi-robot</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-select
                v-model="localObjective.level"
                density="compact"
                :disabled="!enumOptionsLoaded"
                hide-details
                :items="enumOptions.level"
                label="Level"
                :loading="!enumOptionsLoaded"
              />
            </v-col>
            <v-col class="py-1 px-1">
              <v-select
                v-model="localObjective.confidentiality"
                density="compact"
                :disabled="!enumOptionsLoaded"
                hide-details
                :items="enumOptions.confidentiality"
                label="Confidentiality"
                :loading="!enumOptionsLoaded"
              />
            </v-col>
            <v-col class="py-1 px-1">
              <v-select
                v-model="localObjective.strategic_perspective"
                density="compact"
                :disabled="!enumOptionsLoaded"
                hide-details
                :items="enumOptions.strategic_perspective"
                label="Strategic Perspective"
                :loading="!enumOptionsLoaded"
              />
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-select
                v-model="localObjective.priority"
                density="compact"
                :disabled="!enumOptionsLoaded"
                hide-details
                :items="enumOptions.priority"
                label="Priority"
                :loading="!enumOptionsLoaded"
              />
            </v-col>
            <v-col class="py-1 px-1">
              <v-select
                v-model="localObjective.status"
                density="compact"
                :disabled="!enumOptionsLoaded"
                hide-details
                :items="enumOptions.status"
                label="Status"
                :loading="!enumOptionsLoaded"
                required
                :rules="[rules.required]"
              />
            </v-col>
            <v-col class="py-1 px-1">
              <v-select
                v-model="localObjective.review_cadence"
                density="compact"
                :disabled="!enumOptionsLoaded"
                hide-details
                :items="enumOptions.review_cadence"
                label="Review Cadence"
                :loading="!enumOptionsLoaded"
                required
                :rules="[rules.required]"
              />
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-text-field
                v-model="localObjective.start_date"
                density="compact"
                hide-details
                label="Start Date"
                required
                :rules="[rules.required]"
                type="date"
              />
            </v-col>
            <v-col class="py-1 px-1">
              <v-text-field
                v-model="localObjective.target_completion_date"
                density="compact"
                hide-details
                label="Target Date"
                required
                :rules="[rules.required]"
                type="date"
              />
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-select
                v-model="localObjective.owner_id"
                density="compact"
                :disabled="!teamMembersLoaded"
                hide-details
                item-title="title"
                item-value="value"
                :items="teamMembers.map(tm => ({ title: (tm.name || (tm.first_name + ' ' + tm.last_name)) + (tm.position ? ` (${tm.position})` : ''), value: tm.id }))"
                label="Owner"
                :loading="!teamMembersLoaded"
                required
                :rules="[rules.required]"
              />
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-select
                v-model="localObjective.parent_objective_id"
                clearable
                density="compact"
                hide-details
                item-title="title"
                item-value="id"
                :items="parentObjectives"
                label="Parent Objective"
              />
            </v-col>
          </v-row>
        </v-form>
      </v-card-text>
      <v-card-actions class="py-2 px-3">
        <v-spacer />
        <v-btn text @click="onCancel">Cancel</v-btn>
        <v-btn color="primary" @click="onSave">Save</v-btn>
      </v-card-actions>
    </v-card>
    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="4000">
      {{ snackbarText }}
    </v-snackbar>
  </v-dialog>
</template>
<script setup>
  import { computed, ref, watch } from 'vue'
  import api from '@/api'

  const props = defineProps({
    modelValue: Boolean,
    objectiveId: {
      type: Number,
      required: false,
      default: null,
    },
  })
  const emit = defineEmits(['update:modelValue', 'save', 'cancel'])
  const formRef = ref(null)
  const dialogVisible = computed({
    get: () => props.modelValue,
    set: val => emit('update:modelValue', val),
  })

  const localObjective = ref(null)
  const enumOptions = ref({
    priority: [], status: [], level: [], confidentiality: [], strategic_perspective: [], review_cadence: [],
  })
  const enumOptionsLoaded = ref(false)
  const teamMembers = ref([])
  const teamMembersLoaded = ref(false)
  const allObjectives = ref([])
  const loading = ref(false)
  const rewritingDescription = ref(false)
  const rewritingAlignmentStatement = ref(false)
  const rules = { required: v => !!v || 'Required' }

  const snackbar = ref(false)
  const snackbarColor = ref('')
  const snackbarText = ref('')

  const parentObjectives = computed(() =>
    allObjectives.value
      .filter(obj => obj.id !== props.objectiveId)
      .map(obj => ({ id: obj.id, title: obj.title }))
  )

  async function fetchAllData () {
    loading.value = true
    try {
      if (props.objectiveId) {
        const [objRes, enumsRes, membersRes, allObjRes] = await Promise.all([
          api.get(`/objectives/${props.objectiveId}`),
          api.get('/objectives/enums'),
          api.get('/team-members'),
          api.get('/objectives'),
        ])
        localObjective.value = objRes.data
        enumOptions.value = enumsRes.data
        enumOptionsLoaded.value = true
        teamMembers.value = membersRes.data
        teamMembersLoaded.value = true
        allObjectives.value = allObjRes.data
      } else {
        const [enumsRes, membersRes, allObjRes] = await Promise.all([
          api.get('/objectives/enums'),
          api.get('/team-members'),
          api.get('/objectives'),
        ])
        localObjective.value = {
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
          parent_objective_id: null,
          review_cadence: '',
        }
        enumOptions.value = enumsRes.data
        enumOptionsLoaded.value = true
        teamMembers.value = membersRes.data
        teamMembersLoaded.value = true
        allObjectives.value = allObjRes.data
      }
    } catch (e) {
      console.error('Failed to load objective data', e)
      snackbarText.value = 'Failed to load objective data: ' + (e?.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
    } finally {
      loading.value = false
    }
  }

  watch(() => props.objectiveId, fetchAllData, { immediate: true })

  async function rewriteDescription () {
    const originalText = localObjective.value.description
    if (!originalText || !originalText.trim()) return
    rewritingDescription.value = true
    try {
      const res = await api.post('/rewrite-text/rewrite-text', {
        originalText,
        instructions: 'none',
      })
      if (res.data && res.data.rewrittenText) {
        localObjective.value.description = res.data.rewrittenText
      }
    } catch (e) {
      console.error('AI rewrite failed', e)
      snackbarText.value = 'AI rewrite failed: ' + (e?.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
    } finally {
      rewritingDescription.value = false
    }
  }

  async function rewriteAlignmentStatement () {
    const originalText = localObjective.value.alignment_statement
    if (!originalText || !originalText.trim()) return
    rewritingAlignmentStatement.value = true
    try {
      const res = await api.post('/rewrite-text/rewrite-text', {
        originalText,
        instructions: 'none',
      })
      if (res.data && res.data.rewrittenText) {
        localObjective.value.alignment_statement = res.data.rewrittenText
      }
    } catch (e) {
      console.error('AI rewrite failed', e)
      snackbarText.value = 'AI rewrite failed: ' + (e?.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
    } finally {
      rewritingAlignmentStatement.value = false
    }
  }

  function onSave () {
    emit('save', localObjective.value, formRef.value)
  }
  function onCancel () {
    emit('cancel')
    emit('update:modelValue', false)
  }
</script>
