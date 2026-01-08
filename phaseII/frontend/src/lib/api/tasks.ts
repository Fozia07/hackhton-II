import { api } from './client'
import { type Task, type CreateTaskInput, type UpdateTaskInput } from '@/types/task'

export const taskApi = {
  async getAll(): Promise<Task[]> {
    const response = await api.get<{ data: Task[] }>('/api/v1/tasks')
    return response.data
  },

  async create(data: CreateTaskInput): Promise<Task> {
    const response = await api.post<{ data: Task }>('/api/v1/tasks', data)
    return response.data
  },

  async update(id: string, data: UpdateTaskInput): Promise<Task> {
    const response = await api.patch<{ data: Task }>(`/api/v1/tasks/${id}`, data)
    return response.data
  },

  async delete(id: string): Promise<void> {
    await api.delete(`/api/v1/tasks/${id}`)
  },

  async toggleComplete(id: string, completed: boolean): Promise<Task> {
    const response = await api.patch<{ data: Task }>(`/api/v1/tasks/${id}`, { completed })
    return response.data
  },
}