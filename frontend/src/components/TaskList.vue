<template>
  <div>
    <div class="flex items-center justify-between mb-4">
      <label class="flex items-center gap-2">
        Filter by status:
        <select v-model="filterStatus" @change="applyFilter" class="border px-2 py-1 rounded">
          <option value="">All</option>
          <option v-for="s in statuses" :key="s" :value="s">{{ s }}</option>
        </select>
      </label>

      <button
        @click="openAddForm"
        class="bg-blue-600 text-white px-3 py-1 rounded hover:bg-blue-700"
      >
        + Add Task
      </button>
    </div>

    <div v-if="error" class="text-red-600 mb-2">{{ error }}</div>

    <table class="w-full border-collapse border border-gray-300">
      <thead class="bg-gray-100">
        <tr>
          <th class="border px-2 py-1 text-left">ID</th>
          <th class="border px-2 py-1 text-left">Title</th>
          <th class="border px-2 py-1 text-left">Description</th>
          <th class="border px-2 py-1 text-left">Status</th>
          <th class="border px-2 py-1 text-left">Created</th>
          <th class="border px-2 py-1 text-left">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="task in tasks" :key="task.id" class="hover:bg-gray-50">
          <td class="border px-2 py-1">{{ task.id }}</td>
          <td class="border px-2 py-1">{{ task.title }}</td>
          <td class="border px-2 py-1">{{ task.description }}</td>
          <td class="border px-2 py-1">{{ task.status }}</td>
          <td class="border px-2 py-1">{{ dayjs(task.created_at).format('YYYY-MM-DD HH:mm') }}</td>
          <td class="border px-2 py-1 flex gap-2">
            <button @click="openEditForm(task)" class="px-2 py-1 border rounded">Edit</button>
            <button
              @click="removeTask(task.id)"
              class="px-2 py-1 border rounded bg-red-600 text-white hover:bg-red-700"
            >
              Delete
            </button>
          </td>
        </tr>
        <tr v-if="tasks.length === 0">
          <td colspan="6" class="text-center py-2 text-gray-500">No tasks found</td>
        </tr>
      </tbody>
    </table>

    <div class="flex items-center gap-2 mt-3">
      <button
        @click="prevPage"
        :disabled="page === 1"
        class="px-2 py-1 border rounded disabled:opacity-50"
      >
        Prev
      </button>
      <span>Page {{ page }}</span>
      <button
        @click="nextPage"
        :disabled="!hasMore"
        class="px-2 py-1 border rounded disabled:opacity-50"
      >
        Next
      </button>
    </div>

    <div
      v-if="showModal"
      class="fixed inset-0 bg-black bg-opacity-60 flex items-center justify-center z-50"
    >
      <div class="bg-white p-6 rounded-lg shadow-lg w-[400px]">
        <TaskForm :task="editingTask || undefined" @save="onSave" @cancel="closeModal" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import dayjs from 'dayjs';
import TaskForm from './TaskForm.vue';
import { listTasks, createTask, updateTask, deleteTask } from '../api';
import { TaskStatus } from '../types';
import type { Task, TaskCreate, TaskQueryParams, TaskStatusType } from '../types';

const tasks = ref<Task[]>([]);
const page = ref(1);
const perPage = 10;
const hasMore = ref(true);
const filterStatus = ref<string | ''>('');
const error = ref('');

const showModal = ref(false);
const editingTask = ref<Task | null>(null);

const statuses = Object.values(TaskStatus);

async function load() {
  error.value = '';
  try {
    const params: TaskQueryParams = {
      page: page.value,
      per_page: perPage,
      status: filterStatus.value || undefined,
    };
    const data = await listTasks(params);

    if (data.length === 0 && page.value > 1) {
      page.value -= 1;
      await load();
      return;
    }

    tasks.value = data;

    const nextPageData = await listTasks({ ...params, page: page.value + 1 });
    hasMore.value = nextPageData.length > 0;
  } catch (err: any) {
    error.value = err?.message || 'Failed to load tasks';
    tasks.value = [];
    hasMore.value = false;
  }
}

onMounted(load);

function openAddForm() {
  editingTask.value = null;
  showModal.value = true;
}

function openEditForm(task: Task) {
  editingTask.value = task;
  showModal.value = true;
}

function closeModal() {
  showModal.value = false;
}

async function onSave(payload: { title: string; description: string; status?: string | null }) {
  error.value = '';
  const newPayload: TaskCreate = {
    title: payload.title,
    description: payload.description,
    status: payload.status ? (payload.status as TaskStatusType) : undefined,
  };

  try {
    if (editingTask.value) {
      await updateTask(editingTask.value.id, newPayload);
    } else {
      await createTask(newPayload);
    }
    closeModal();
    await load();
  } catch (err: any) {
    error.value = err?.message || 'Failed to save task';
  }
}

async function removeTask(id: number) {
  error.value = '';
  try {
    await deleteTask(id);
    await load();
  } catch (err: any) {
    error.value = err?.message || 'Failed to delete task';
  }
}

function nextPage() {
  if (!hasMore.value) return;
  page.value += 1;
  load();
}

function prevPage() {
  if (page.value === 1) return;
  page.value -= 1;
  load();
}

function applyFilter() {
  page.value = 1;
  load();
}
</script>
