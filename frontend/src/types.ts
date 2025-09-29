export const TaskStatus = {
  TODO: 'To Do',
  IN_PROGRESS: 'In Progress',
  DONE: 'Done',
} as const;

export type TaskStatusType = (typeof TaskStatus)[keyof typeof TaskStatus];

export interface Task {
  id: number;
  title: string;
  description: string;
  status: TaskStatusType;
  created_at: string;
}

export type TaskCreate = {
  title: string;
  description: string;
  status?: TaskStatusType;
};

export type TaskUpdate = Partial<TaskCreate>;

export interface TaskQueryParams {
  status?: string | null;
  page?: number;
  per_page?: number;
  sort_order?: 'asc' | 'desc';
}
