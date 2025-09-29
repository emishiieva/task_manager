<template>
  <div class="min-h-screen bg-gray-50 p-6">
    <div class="max-w-5xl mx-auto">
      <h1 class="text-2xl font-semibold mb-4">Task Manager</h1>
      <TaskList />
    </div>
  </div>
</template>

<script setup lang="ts">
import TaskList from './components/TaskList.vue';
</script>
