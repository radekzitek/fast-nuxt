<template>
  <div :class="['tree-node', { root: level === 0 }]" :style="{ marginLeft: `${level * 2}rem` }">
    <div class="node-content">
      <v-avatar class="avatar" size="32">
        <v-icon>mdi-account-circle</v-icon>
      </v-avatar>
      <span class="name">{{ member.first_name }} {{ member.last_name }}</span>
      <span v-if="member.position" class="position">({{ member.position }})</span>
    </div>
    <div v-if="member.subordinates && member.subordinates.length" class="subordinates">
      <div v-for="sub in member.subordinates" :key="sub.id" class="subordinate-line">
        <TeamTreeNode :level="level + 1" :member="sub" />
      </div>
    </div>
  </div>
</template>

<script setup>
  import { defineProps } from 'vue';
  defineProps({
    member: { type: Object, required: true },
    level: { type: Number, required: true },
  });
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
</style>
