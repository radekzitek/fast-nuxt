<template>
  <v-dialog v-model="dialogVisible" max-width="500px">
    <v-card>
      <v-card-title class="py-2 px-3">
        <span class="text-h6">{{ isEdit ? 'Edit User' : 'Create User' }}</span>
      </v-card-title>
      <v-card-text class="py-2 px-3">
        <v-form ref="formRef" @submit.prevent="onSave">
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-text-field
                v-model="localUser.username"
                density="compact"
                hide-details
                label="Username"
                required
                :rules="[rules.required]"
              />
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-text-field
                v-model="localUser.first_name"
                density="compact"
                hide-details
                label="First Name"
                required
                :rules="[rules.required]"
              />
            </v-col>
            <v-col class="py-1 px-1">
              <v-text-field
                v-model="localUser.last_name"
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
                v-model="localUser.email"
                density="compact"
                hide-details
                label="Email"
                required
                :rules="[rules.required, rules.email]"
              />
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-text-field
                v-if="!isEdit || showPassword"
                v-model="localUser.password"
                :append-icon="showPassword ? 'mdi-eye-off' : 'mdi-eye'"
                density="compact"
                hide-details
                label="Password"
                :required="!isEdit"
                :rules="!isEdit ? [rules.required] : []"
                :type="showPassword ? 'text' : 'password'"
                @click:append="showPassword = !showPassword"
              />
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-select
                v-model="localUser.team_member_id"
                clearable
                density="compact"
                hide-details
                :item-title="tm => `${tm.first_name} ${tm.last_name}${tm.position ? ' (' + tm.position + ')' : ''}`"
                item-value="id"
                :items="allTeamMembers"
                label="Team Member"
              />
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-textarea v-model="localUser.note" density="compact" hide-details label="Note" />
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-switch v-model="localUser.active" hide-details label="Active" />
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
    userId: {
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
  const isEdit = computed(() => !!props.userId)
  const showPassword = ref(false)
  const localUser = ref({
    id: null,
    username: '',
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    note: '',
    active: true,
    team_member_id: null,
  })
  const allTeamMembers = ref([])
  const loading = ref(false)
  const rules = {
    required: v => !!v || 'Required',
    email: v => !v || /.+@.+\..+/.test(v) || 'E-mail must be valid',
  }
  const snackbar = ref(false)
  const snackbarColor = ref('')
  const snackbarText = ref('')
  async function fetchAllTeamMembers () {
    try {
      const res = await api.get('/team-members');
      allTeamMembers.value = res.data;
    } catch (e) {
      allTeamMembers.value = [];
      snackbarText.value = 'Failed to load team members: ' + (e?.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
    }
  }
  async function fetchUserData () {
    loading.value = true
    try {
      await fetchAllTeamMembers()
      if (props.userId) {
        const res = await api.get(`/users/${props.userId}`)
        localUser.value = {
          ...res.data,
          password: '',
        }
      } else {
        localUser.value = {
          id: null,
          username: '',
          first_name: '',
          last_name: '',
          email: '',
          password: '',
          note: '',
          active: true,
          team_member_id: null,
        }
      }
    } catch (e) {
      snackbarText.value = 'Failed to load user data: ' + (e?.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
    } finally {
      loading.value = false
    }
  }
  watch(() => props.userId, fetchUserData, { immediate: true })
  function onSave () {
    emit('save', localUser.value, formRef.value)
  }
  function onCancel () {
    emit('cancel')
    emit('update:modelValue', false)
  }
</script>
