<template>
  <v-card class="pa-3 mb-4" outlined>
    <div class="d-flex align-center mb-2">
      <v-icon class="mr-2" color="primary">mdi-chart-line</v-icon>
      <span class="text-h6">Progress Analysis</span>
      <v-spacer />
      <v-btn
        :disabled="loading"
        icon
        size="small"
        :title="'Refresh analysis'"
        @click="reload"
      >
        <v-icon>mdi-refresh</v-icon>
      </v-btn>
    </div>
    <div v-if="loading">
      <v-progress-circular color="primary" indeterminate /> Loading analysis...
    </div>
    <div v-else-if="objective">
      <v-row>
        <v-col cols="12" md="6">
          <div>Today: <b>{{ today }}</b></div>
          <div class="my-2">
            <v-progress-linear
              color="primary"
              height="18"
              :max="100"
              :model-value="expectedProgress"
              rounded
            >
              <template #default>
                <span style="font-size: 1em;">Expected progress today: <b>{{ expectedProgress }}%</b></span>
              </template>
            </v-progress-linear>
          </div>
          <div class="my-2">
            <v-progress-linear
              :color="mostRecentUpdate && mostRecentUpdate.progress >= expectedProgress ? 'success' : 'error'"
              height="14"
              :max="100"
              :model-value="mostRecentUpdate ? mostRecentUpdate.progress : 0"
              rounded
            >
              <template #default>
                <span style="font-size: 0.95em;">Most recent reported: <b>{{ mostRecentUpdate ? (mostRecentUpdate.progress + '%') : '-' }}</b></span>
              </template>
            </v-progress-linear>
          </div>
          <div v-if="expectedProgress === 0" class="text-grey">Objective has not started yet.</div>
          <div v-else-if="expectedProgress === 100" class="text-success">Target date reached or passed.</div>
          <div v-if="mostRecentUpdate">
            <div v-if="recommendation.status === 'ON_TRACK'" class="mt-2 text-success">
              <v-icon class="mr-1" color="success">mdi-thumb-up</v-icon>
              Recommendation: <b>ON_TRACK</b> (progress is better than expected)
            </div>
            <div v-else-if="recommendation.status === 'DELAYED'" class="mt-2 text-error">
              <v-icon class="mr-1" color="error">mdi-alert</v-icon>
              Recommendation: <b>DELAYED</b> (progress is worse than expected)
            </div>
            <div v-else-if="recommendation.status === 'AT_RISK'" class="mt-2" style="color: orange;">
              <v-icon class="mr-1" color="orange">mdi-alert</v-icon>
              Recommendation: <b>AT_RISK</b> (progress is mixed)
            </div>
          </div>
        </v-col>
        <v-col v-if="mostRecentUpdate" cols="12" md="6">
          <div>Most recent progress update: <b>{{ mostRecentUpdate.progress_date }}</b></div>
          <div class="my-2">
            <v-progress-linear
              color="primary"
              height="16"
              :max="100"
              :model-value="expectedProgressAtLastUpdate"
              rounded
            >
              <template #default>
                <span style="font-size: 1em;">Expected progress at that date: <b>{{ expectedProgressAtLastUpdate }}%</b></span>
              </template>
            </v-progress-linear>
          </div>
          <div class="my-2">
            <v-progress-linear
              :color="mostRecentUpdate.progress >= expectedProgressAtLastUpdate ? 'success' : 'error'"
              height="14"
              :max="100"
              :model-value="mostRecentUpdate.progress"
              rounded
            >
              <template #default>
                <span style="font-size: 0.95em;">Most recent reported: <b>{{ mostRecentUpdate.progress + '%' }}</b></span>
              </template>
            </v-progress-linear>
          </div>
          <div v-if="isOverdue" class="text-error mt-2">
            <v-icon class="mr-1" color="error">mdi-alert</v-icon>
            Progress update is overdue! Last update was {{ daysSinceLastUpdate }} days ago (review cadence: {{ reviewCadenceDays }} days).
          </div>
          <div v-else-if="mostRecentUpdate && reviewCadenceDays" class="text-green mt-2">
            <v-icon class="mr-1" color="green">mdi-calendar-clock</v-icon>
            Next progress update due: <b>{{ nextDueDate }}</b>
          </div>
        </v-col>
      </v-row>
    </div>
    <div v-else class="text-error">Objective not found.</div>
    <v-snackbar v-model="snackbar" :color="snackbarColor" timeout="4000">
      {{ snackbarText }}
    </v-snackbar>
  </v-card>
</template>
<script setup>
  import { computed, onMounted, ref, watch } from 'vue'
  import api from '@/api'
  import { differenceInDays } from 'date-fns'

  const props = defineProps({
    objectiveId: {
      type: Number,
      required: true,
    },
  })
  const objective = ref(null)
  const loading = ref(false)
  const today = new Date().toISOString().slice(0, 10)
  const mostRecentUpdate = ref(null)
  const snackbar = ref(false)
  const snackbarColor = ref('error')
  const snackbarText = ref('')

  const expectedProgress = computed(() => {
    if (!objective.value) return 0
    const start = new Date(objective.value.start_date)
    const target = new Date(objective.value.target_completion_date)
    const now = new Date(today)
    if (now < start) return 0
    if (now >= target) return 100
    const total = target - start
    const elapsed = now - start
    if (total <= 0) return 100
    return Math.round((elapsed / total) * 100)
  })

  const expectedProgressAtLastUpdate = computed(() => {
    if (!objective.value || !mostRecentUpdate.value) return null
    const start = new Date(objective.value.start_date)
    const target = new Date(objective.value.target_completion_date)
    const updateDate = new Date(mostRecentUpdate.value.progress_date)
    if (updateDate < start) return 0
    if (updateDate >= target) return 100
    const total = target - start
    const elapsed = updateDate - start
    if (total <= 0) return 100
    return Math.round((elapsed / total) * 100)
  })

  const reviewCadenceDays = computed(() => {
    if (!objective.value || !objective.value.review_cadence) return null
    switch (objective.value.review_cadence) {
      case 'MONTHLY': return 30
      case 'QUARTERLY': return 90
      case 'BI_ANNUALLY': return 182
      case 'ANNUALLY': return 365
      default: return null
    }
  })

  const daysSinceLastUpdate = computed(() => {
    if (!mostRecentUpdate.value) return null
    const lastDate = new Date(mostRecentUpdate.value.progress_date)
    const now = new Date(today)
    return differenceInDays(now, lastDate)
  })

  const isOverdue = computed(() => {
    if (!reviewCadenceDays.value || daysSinceLastUpdate.value === null) return false
    return daysSinceLastUpdate.value > reviewCadenceDays.value
  })

  const nextDueDate = computed(() => {
    if (!mostRecentUpdate.value || !reviewCadenceDays.value) return null
    const lastDate = new Date(mostRecentUpdate.value.progress_date)
    const due = new Date(lastDate.getTime() + reviewCadenceDays.value * 24 * 60 * 60 * 1000)
    return due.toISOString().slice(0, 10)
  })

  const recommendation = computed(() => {
    if (!mostRecentUpdate.value) return { status: null }
    const progress = mostRecentUpdate.value.progress
    const betterToday = progress >= expectedProgress.value
    const betterAtLast = expectedProgressAtLastUpdate.value !== null && progress >= expectedProgressAtLastUpdate.value
    if (betterToday && betterAtLast) return { status: 'ON_TRACK' }
    if (!betterToday && !betterAtLast) return { status: 'DELAYED' }
    if ((betterToday && !betterAtLast) || (!betterToday && betterAtLast)) return { status: 'AT_RISK' }
    return { status: null }
  })

  async function loadObjective () {
    loading.value = true
    try {
      const res = await api.get(`/objectives/${props.objectiveId}`)
      objective.value = res.data
      await loadMostRecentProgressUpdate()
    } catch (e) {
      objective.value = null
      snackbarText.value = 'Failed to load objective: ' + (e?.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
    } finally {
      loading.value = false
    }
  }

  async function loadMostRecentProgressUpdate () {
    try {
      const res = await api.get(`/objectives/${props.objectiveId}/progress-updates`)
      if (Array.isArray(res.data) && res.data.length > 0) {
        mostRecentUpdate.value = res.data.reduce((max, curr) =>
                                                   new Date(curr.progress_date) > new Date(max.progress_date) ? curr : max,
                                                 res.data[0]
        )
      } else {
        mostRecentUpdate.value = null
      }
    } catch (e) {
      mostRecentUpdate.value = null
      snackbarText.value = 'Failed to load progress updates: ' + (e?.response?.data?.detail || e.message)
      snackbarColor.value = 'error'
      snackbar.value = true
    }
  }

  function reload () {
    loadObjective();
  }

  onMounted(loadObjective)
  watch(() => props.objectiveId, loadObjective)
</script>
