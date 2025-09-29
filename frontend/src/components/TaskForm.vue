<template>
  <form @submit.prevent="onSubmit" class="space-y-4">
    <div>
      <label class="block text-sm font-medium text-gray-700">Title</label>
      <input
        v-model="title"
        type="text"
        placeholder="Enter title"
        class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
      />
      <p v-if="errorTitle" class="text-red-600 text-sm mt-1">{{ errorTitle }}</p>
      <p v-if="serverError" class="text-red-600 text-sm mt-1">{{ serverError }}</p>
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700">Description</label>
      <textarea
        v-model="description"
        rows="4"
        placeholder="Enter description"
        class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
      ></textarea>
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700">Status</label>
      <select
        v-model="status"
        class="mt-1 block w-full p-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
      >
        <option :value="null">-- choose --</option>
        <option v-for="s in statuses" :key="s" :value="s">{{ s }}</option>
      </select>
    </div>

    <div class="flex justify-end gap-2">
      <button
        type="button"
        @click="onCancel"
        class="px-4 py-2 rounded-md border border-gray-300 text-gray-700 hover:bg-gray-100"
      >
        Cancel
      </button>
      <button type="submit" class="px-4 py-2 rounded-md bg-blue-600 text-white hover:bg-blue-700">
        Save
      </button>
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue';
import { TaskStatus } from '../types';
import type { Task, TaskStatusType } from '../types';

const props = defineProps<{ task?: Task }>();
const emit = defineEmits<{
  // eslint-disable-next-line no-unused-vars
  (e: 'save', payload: { title: string; description: string; status?: TaskStatusType }): void;
  // eslint-disable-next-line no-unused-vars
  (e: 'cancel'): void;
}>();

const title = ref(props.task?.title ?? '');
const description = ref(props.task?.description ?? '');
const status = ref<TaskStatusType | null>(props.task?.status ?? null);
const errorTitle = ref('');
const serverError = ref('');

watch(
  () => props.task,
  (t) => {
    title.value = t?.title ?? '';
    description.value = t?.description ?? '';
    status.value = t?.status ?? null;
    serverError.value = '';
  },
);

const statuses = Object.values(TaskStatus);

function validate() {
  errorTitle.value = '';
  if (!title.value.trim()) {
    errorTitle.value = 'Title is required';
    return false;
  }
  return true;
}

async function onSubmit() {
  if (!validate()) return;
  serverError.value = '';

  try {
    emit('save', {
      title: title.value.trim(),
      description: description.value.trim(),
      status: status.value ?? undefined,
    });
  } catch (err: any) {
    serverError.value = err?.response?.data?.message || 'Server error';
  }
}

function onCancel() {
  emit('cancel');
}
</script>
