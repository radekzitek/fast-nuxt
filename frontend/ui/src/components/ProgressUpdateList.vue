<template>
  <v-table v-if="progressUpdates.length">
    <thead>
      <tr>
        <th>Date</th>
        <th>Comment</th>
        <th>Progress</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="update in progressUpdates" :key="update.id">
        <td>{{ update.progress_date }}</td>
        <td style="white-space: pre-line;">{{ update.comment }}</td>
        <td>
          <div style="min-width: 100px;">
            <v-progress-linear
              color="primary"
              height="16"
              :max="100"
              :model-value="update.progress || 0"
              rounded
              style="margin-bottom: 2px;"
            />
            <span style="font-size: 0.95em;">{{ update.progress !== null && update.progress !== undefined ? update.progress + ' %' : '-' }}</span>
          </div>
        </td>
        <td>
          <v-btn icon size="small" @click="$emit('edit', update)">
            <v-icon>mdi-pencil</v-icon>
          </v-btn>
          <v-btn color="error" icon size="small" @click="$emit('delete', update)">
            <v-icon>mdi-delete</v-icon>
          </v-btn>
        </td>
      </tr>
    </tbody>
  </v-table>
  <div v-else class="text-grey">No progress updates yet.</div>
</template>

<script setup>
  defineProps({
    progressUpdates: Array,
  })
  defineEmits(['edit', 'delete'])
</script>
