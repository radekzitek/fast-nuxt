<template>
  <div :class="['tree-node', { root: level === 0 }]" :style="{ marginLeft: `${level * 2}rem` }">
    <div class="node-content">
      <v-avatar class="avatar" size="32">
        <v-icon>mdi-account-circle</v-icon>
      </v-avatar>
      <span class="name" style="cursor:pointer; text-decoration:underline;" @click="$emit('edit-team-member', member)">{{ member.first_name }} {{ member.last_name }}</span>
      <span v-if="member.position" class="position">({{ member.position }})</span>
      <div v-if="objectivesLoading" class="objectives-loading">
        <v-icon color="primary" size="32">mdi-flag-variant</v-icon>
        <span>Loading objectives...</span>
      </div>
      <div v-if="objectivesError" class="objectives-error">
        <v-icon color="error" size="32">mdi-alert-circle</v-icon>
        <span>Failed to load objectives: {{ objectivesError }}</span>
      </div>
      <div v-if="objectives.length" class="objectives-list">
        <div v-for="obj in objectives" :key="obj.id" class="objective-item">
          <v-icon :color="getObjectiveColor(obj.status)" size="32">mdi-flag-variant</v-icon>
          <span class="objective-title" style="cursor:pointer; text-decoration:underline;" @click="$emit('edit-objective', obj)">{{ obj.title }}</span>
          <v-icon color="#888" size="18" style="margin-left:2px; cursor:pointer;" @click="goToObjectiveDashboard(obj.id)">mdi-dots-horizontal</v-icon>
        </div>
      </div>
    </div>

    <div v-if="member.subordinates && member.subordinates.length" class="subordinates">
      <div v-for="sub in member.subordinates" :key="sub.id" class="subordinate-line">
        <TeamTreeNode
          :level="level + 1"
          :member="sub"
          @edit-objective="$emit('edit-objective', $event)"
          @edit-team-member="$emit('edit-team-member', $event)"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref, watch } from 'vue'
  import api from '@/api'
  import { useRouter } from 'vue-router'

  const props = defineProps({
    member: { type: Object, required: true },
    level: { type: Number, required: true },
  });

  defineEmits(['edit-objective', 'edit-team-member'])

  const objectives = ref([])
  const objectivesLoading = ref(false)
  const objectivesError = ref(null)
  const router = useRouter()

  async function fetchObjectivesForMember (memberId) {
    objectivesLoading.value = true
    objectivesError.value = null
    try {
      const res = await api.get(`/team-members/${memberId}/objectives`)
      objectives.value = res.data
    } catch (e) {
      objectivesError.value = e?.response?.data?.detail || e.message
    } finally {
      objectivesLoading.value = false
    }
  }

  function getObjectiveColor (status) {
    switch (status) {
      case 'ON_TRACK': return 'lime';
      case 'NOT_STARTED': return 'blue';
      case 'AT_RISK': return 'orange';
      case 'DELAYED': return 'red';
      case 'ACHIEVED': return 'green';
      case 'ON_HOLD': return 'yellow';
      case 'CANCELLED': return 'brown';
      default: return 'grey';
    }
  }

  function goToObjectiveDashboard (id) {
    router.push({ path: `/objective-dashboard/${id}` })
  }

  watch(() => props.member.id, id => {
    if (id) fetchObjectivesForMember(id)
  }, { immediate: true })
</script>

<style scoped>
.tree-node {
  position: relative;
  padding: 0.5rem 0 0.5rem 0.5rem;
}
.node-content {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #f5f7fa;
  border-radius: 6px;
  padding: 0.5rem 1rem;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.avatar {
  background: #1976d2;
  color: #fff;
}
.name {
  font-weight: 600;
  color: #222;
}
.position {
  color: #888;
  font-size: 0.95em;
  margin-left: 0.5em;
}
.subordinates {
  margin-left: 1.5rem;
  border-left: 2px solid #e0e0e0;
  padding-left: 0.5rem;
}
.subordinate-line {
  margin-top: 0.5rem;
}
.root > .node-content {
  background: #e3f2fd;
  border: 2px solid #1976d2;
}
.objectives-list {
  margin-left: 2.5rem;
  margin-top: 0.2rem;
}
.objective-item {
  display: flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.9em;
}
.objectives-loading, .objectives-error {
  margin-left: 2.5rem;
  font-size: 0.95em;
  color: #888;
  display: flex;
  align-items: center;
  gap: 0.3rem;
}
</style>
