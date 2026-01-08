import { z } from 'zod'

export const taskSchema = z.object({
  title: z.string()
    .min(1, 'Task title is required')
    .max(500, 'Task title must be less than 500 characters'),
})

export const updateTaskSchema = z.object({
  title: z.string()
    .min(1, 'Task title is required')
    .max(500, 'Task title must be less than 500 characters')
    .optional(),
  completed: z.boolean().optional(),
})