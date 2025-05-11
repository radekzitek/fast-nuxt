<template>
  <v-dialog v-model="dialog" max-width="400px">
    <v-card>
      <v-card-title class="text-h6">Confirm Delete</v-card-title>
      <v-card-text>
        Are you sure you want to delete this progress update?
        <div class="mt-2"><b>{{ progressUpdate?.comment }}</b></div>
      </v-card-text>
      <v-card-actions>
        <v-spacer />
        <v-btn text @click="$emit('cancel')">Cancel</v-btn>
        <v-btn color="error" @click="$emit('delete')">Delete</v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
  import { ref, watch } from 'vue'
  const props = defineProps({
    modelValue: Boolean,
    progressUpdate: Object,
  })
  const emit = defineEmits(['cancel', 'delete', 'update:modelValue'])

  const dialog = ref(props.modelValue)

  watch(() => props.modelValue, val => {
    dialog.value = val
  })

  watch(dialog, val => {
    if (val !== props.modelValue) {
      emit('update:modelValue', val)
    }
  })
</script>
