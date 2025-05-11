<template>
  <div class="team-tree">
    <template v-if="rootMember">
      <TeamTreeNode
        :level="0"
        :member="rootMember"
        @edit-objective="$emit('edit-objective', $event)"
        @edit-team-member="$emit('edit-team-member', $event)"
      />
    </template>
    <template v-else>
      <div class="loading">Loading team structure...</div>
    </template>
  </div>
</template>

<script setup>
  import { computed, defineAsyncComponent } from 'vue';

  defineEmits(['edit-objective', 'edit-team-member']);

  const TeamTreeNode = defineAsyncComponent(() => import('./TeamTreeNode.vue'));

  const props = defineProps({
    members: {
      type: Array,
      required: true,
    },
    userTeamMemberId: {
      type: Number,
      required: true,
    },
  });

  // Build a map of members by id
  const memberMap = computed(() => {
    const map = {};
    props.members.forEach(m => { map[m.id] = { ...m, subordinates: [] }; });
    props.members.forEach(m => {
      if (m.supervisor_id && map[m.supervisor_id]) {
        map[m.supervisor_id].subordinates.push(map[m.id]);
      }
    });
    return map;
  });

  const rootMember = computed(() => memberMap.value[props.userTeamMemberId]);
</script>

<style scoped>
.team-tree {
  margin: 2rem 0;
  padding-left: 1rem;
}
.loading {
  color: #888;
  font-style: italic;
}
</style>
