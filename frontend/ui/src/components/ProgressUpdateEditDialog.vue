<template>
  <v-dialog v-model="dialogVisible" max-width="500px">
    <v-card>
      <v-card-title class="py-2 px-3">
        <span class="text-h6">{{ isEdit ? 'Edit Progress Update' : 'New Progress Update' }}</span>
      </v-card-title>
      <v-card-text class="py-2 px-3">
        <v-form ref="formRef" @submit.prevent="onSave">
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-text-field
                v-model="localProgressUpdate.progress_date"
                density="compact"
                hide-details
                label="Date"
                required
                :rules="[rules.required]"
                type="date"
              />
            </v-col>
            <v-col class="py-1 px-1">
              <v-text-field
                v-model="localProgressUpdate.progress"
                density="compact"
                hide-details
                label="Progress (%)"
                max="100"
                min="0"
                step="0.01"
                type="number"
              />
            </v-col>
          </v-row>
          <v-row class="my-0" dense>
            <v-col class="py-1 px-1">
              <v-textarea
                v-model="localProgressUpdate.comment"
                auto-grow
                density="compact"
                hide-details
                label="Comment"
                required
                :rules="[rules.required]"
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
  // import api from '@/api'

  const props = defineProps({
    modelValue: Boolean,
    progressUpdate: Object,
    objectiveId: Number,
  })
  const emit = defineEmits(['update:modelValue', 'save', 'cancel'])
  const formRef = ref(null)
  const dialogVisible = computed({
    get: () => props.modelValue,
    set: val => emit('update:modelValue', val),
  })
  const isEdit = computed(() => !!(props.progressUpdate && props.progressUpdate.id))
  const localProgressUpdate = ref({
    progress_date: '',
    comment: '',
    progress: null,
  })
  const snackbar = ref(false)
  const snackbarColor = ref('')
  const snackbarText = ref('')
  const rules = { required: v => !!v || 'Required' }

  watch(() => props.progressUpdate, val => {
    if (val) {
      localProgressUpdate.value = { ...val }
    } else {
      localProgressUpdate.value = {
        progress_date: new Date().toISOString().slice(0, 10),
        comment: '',
        progress: null,
      }
    }
  }, { immediate: true })

  function onSave () {
    if (formRef.value && formRef.value.validate && !formRef.value.validate()) return
    emit('save', { ...localProgressUpdate.value, objective_id: props.objectiveId }, formRef.value)
  }
  function onCancel () {
    emit('cancel')
    emit('update:modelValue', false)
  }
</script>
