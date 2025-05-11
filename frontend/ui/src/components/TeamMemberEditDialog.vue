<template>
  <v-dialog v-model="dialogVisible" max-width="500px">
    <v-card>
      <v-card-title class="py-2 px-3">
        <span class="text-h6">{{ isEdit ? 'Edit Team Member' : 'Create Team Member' }}</span>
      </v-card-title>
      <v-card-text class="py-2 px-3">
        <v-form ref="formRef" @submit.prevent="onSave">
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-text-field
                v-model="localTeamMember.first_name"
                density="compact"
                hide-details
                label="First Name"
                required
                :rules="[rules.required]"
              />
            </v-col>
            <v-col class="py-1 px-1">
              <v-text-field
                v-model="localTeamMember.last_name"
                density="compact"
                hide-details
                label="Last Name"
                required
                :rules="[rules.required]"
              />
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-text-field
                v-model="localTeamMember.email"
                density="compact"
                hide-details
                label="Email"
                required
                :rules="[rules.required, rules.email]"
              />
            </v-col>
            <v-col class="py-1 px-1">
              <v-text-field v-model="localTeamMember.phone_number" density="compact" hide-details label="Phone Number" />
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-text-field v-model="localTeamMember.position" density="compact" hide-details label="Position" />
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-select
                v-model="localTeamMember.supervisor_id"
                clearable
                density="compact"
                hide-details
                :item-title="tm => `${tm.first_name} ${tm.last_name}${tm.position ? ' (' + tm.position + ')' : ''}`"
                item-value="id"
                :items="supervisorOptions"
                label="Supervisor"
              />
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-textarea v-model="localTeamMember.notes" density="compact" hide-details label="Notes" />
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
    teamMemberId: {
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
  const isEdit = computed(() => !!props.teamMemberId)
  const localTeamMember = ref({
    id: null,
    first_name: '',
    last_name: '',
    email: '',
    phone_number: '',
    position: '',
    notes: '',
    supervisor_id: null,
  })
  const allTeamMembers = ref([])
  const loading = ref(false)
  const rules = {
    required: v => !!v || 'Required',
    email: v => !v || /.+@.+\..+/.test(v) || 'E-mail must be valid',
  }
  const supervisorOptions = computed(() => {
    if (!localTeamMember.value.id) return allTeamMembers.value
    return allTeamMembers.value.filter(tm => tm.id !== localTeamMember.value.id)
  })

  const snackbar = ref(false)
  const snackbarColor = ref('')
  const snackbarText = ref('')

  async function fetchData () {
    loading.value = true
    try {
      const [membersRes, memberRes] = await Promise.all([
        api.get('/team-members'),
        props.teamMemberId ? api.get(`/team-members/${props.teamMemberId}`) : Promise.resolve({ data: null }),
      ])
      allTeamMembers.value = membersRes.data
      if (props.teamMemberId && memberRes.data) {
        localTeamMember.value = { ...memberRes.data }
      } else {
        localTeamMember.value = {
          id: null,
          first_name: '',
          last_name: '',
          email: '',
          phone_number: '',
          position: '',
          notes: '',
          supervisor_id: null,
        }
      }
    } catch (e) {
      snackbarText.value = 'Failed to load team member data: ' + (e?.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
      console.error('Failed to load team member data', e)
    } finally {
      loading.value = false
    }
  }

  watch(() => props.teamMemberId, fetchData, { immediate: true })

  function onSave () {
    emit('save', localTeamMember.value, formRef.value)
  }
  function onCancel () {
    emit('cancel')
    emit('update:modelValue', false)
  }
</script>
