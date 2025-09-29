import axios from 'axios';
import type { Task, TaskCreate, TaskQueryParams, TaskUpdate } from './types';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: { 'Content-Type': 'application/json' },
});

async function handleRequest<T>(request: Promise<{ data: T }>) {
  try {
    const resp = await request;
    return resp.data;
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
  } catch (err: any) {
    if (err.response?.data?.message) throw new Error(err.response.data.message);
    throw new Error('Network or server error');
  }
}

export async function listTasks(params: TaskQueryParams = {}) {
  return handleRequest(api.get<Task[]>('/api/tasks', { params }));
}

export async function createTask(payload: TaskCreate) {
  return handleRequest(api.post<Task>('/api/tasks', payload));
}

export async function updateTask(id: number, payload: TaskUpdate) {
  return handleRequest(api.put<Task>(`/api/tasks/${id}`, payload));
}

export async function deleteTask(id: number) {
  return handleRequest(api.delete(`/api/tasks/${id}`));
}

export async function getTask(id: number) {
  return handleRequest(api.get<Task>(`/api/tasks/${id}`));
}
