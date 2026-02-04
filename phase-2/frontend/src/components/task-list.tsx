"use client";

import { useState } from "react";
import { fetchWithAuth } from "@/lib/api-client";

interface Task {
  id: number; 
  title: string;
  description?: string;
  completed: boolean; 
  user_id: string;
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  tasks: Task[];
  onTaskUpdated: () => void;
}

export function TaskList({ tasks, onTaskUpdated }: TaskListProps) {
  const [processingId, setProcessingId] = useState<number | null>(null);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState("");
  const [editDescription, setEditDescription] = useState("");

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString(undefined, {
      month: "short",
      day: "numeric",
    });
  };

  const startEditing = (task: Task) => {
    setEditingId(task.id);
    setEditTitle(task.title);
    setEditDescription(task.description || "");
  };

  const cancelEditing = () => {
    setEditingId(null);
    setEditTitle("");
    setEditDescription("");
  };

  const saveTask = async (taskId: number) => {
    if (!editTitle.trim()) return;
    
    setProcessingId(taskId);
    try {
      await fetchWithAuth(`/api/tasks/${taskId}`, {
        method: "PATCH",
        body: JSON.stringify({ 
          title: editTitle,
          description: editDescription || null 
        }),
      });
      setEditingId(null);
      onTaskUpdated();
    } catch (error) {
      console.error("Failed to update task", error);
    } finally {
      setProcessingId(null);
    }
  };

  const toggleCompletion = async (task: Task) => {
    setProcessingId(task.id);
    try {
      await fetchWithAuth(`/api/tasks/${task.id}`, {
        method: "PATCH",
        body: JSON.stringify({ completed: !task.completed }),
      });
      onTaskUpdated();
    } catch (error) {
      console.error("Failed to update task", error);
    } finally {
      setProcessingId(null);
    }
  };

  const deleteTask = async (taskId: number) => {
    if (!confirm("Are you sure you want to delete this task?")) return;
    
    setProcessingId(taskId);
    try {
      await fetchWithAuth(`/api/tasks/${taskId}`, {
        method: "DELETE",
      });
      onTaskUpdated();
    } catch (error) {
      console.error("Failed to delete task", error);
    } finally {
        setProcessingId(null);
    }
  };

  if (tasks.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 px-4 text-center bg-white dark:bg-zinc-900 rounded-xl border border-dashed border-gray-300 dark:border-zinc-700">
        <div className="bg-gray-50 dark:bg-zinc-800 p-4 rounded-full mb-4">
          <svg className="w-8 h-8 text-gray-400 dark:text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <h3 className="text-lg font-medium text-gray-900 dark:text-white">No tasks yet</h3>
        <p className="mt-1 text-sm text-gray-500 dark:text-gray-400 max-w-sm">
          Get started by creating a new task above.
        </p>
      </div>
    );
  }

  return (
    <ul className="space-y-4">
      {tasks.map((task) => (
        <li
          key={task.id}
          className={`group relative overflow-hidden bg-white dark:bg-zinc-900 rounded-xl border transition-all duration-200 hover:shadow-md ${
            task.completed 
              ? "border-gray-200 dark:border-zinc-800 bg-gray-50/50 dark:bg-zinc-900/50" 
              : "border-gray-200 dark:border-zinc-800 hover:border-black/10 dark:hover:border-white/10"
          }`}
        >
          {editingId === task.id ? (
            <div className="p-4 space-y-3">
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent dark:bg-zinc-800 dark:border-zinc-700 dark:text-white"
                placeholder="Task Title"
                autoFocus
              />
              <textarea
                value={editDescription}
                onChange={(e) => setEditDescription(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-black focus:border-transparent dark:bg-zinc-800 dark:border-zinc-700 dark:text-white resize-none"
                placeholder="Description"
                rows={2}
              />
              <div className="flex gap-2 justify-end">
                <button
                  onClick={cancelEditing}
                  className="px-3 py-1.5 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 dark:text-gray-300 dark:bg-zinc-800 dark:hover:bg-zinc-700"
                >
                  Cancel
                </button>
                <button
                  onClick={() => saveTask(task.id)}
                  disabled={processingId === task.id}
                  className="px-3 py-1.5 text-sm font-medium text-white bg-black rounded-lg hover:bg-zinc-800 dark:bg-white dark:text-black dark:hover:bg-zinc-200"
                >
                  Save Changes
                </button>
              </div>
            </div>
          ) : (
            <div className="flex items-start p-4 sm:p-5 gap-4">
              <div className="pt-0.5">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => toggleCompletion(task)}
                  disabled={processingId === task.id}
                  className="h-5 w-5 rounded-md border-gray-300 text-black focus:ring-black focus:ring-offset-0 cursor-pointer dark:border-zinc-600 dark:bg-zinc-800 dark:checked:bg-white dark:checked:border-white transition-all"
                />
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 flex-wrap">
                  <h3 className={`text-base font-semibold truncate transition-colors duration-200 ${
                    task.completed 
                      ? "text-gray-500 line-through decoration-gray-400" 
                      : "text-gray-900 dark:text-white"
                  }`}>
                    {task.title}
                  </h3>
                  {task.completed && (
                    <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-600 dark:bg-zinc-800 dark:text-zinc-400">
                      Completed
                    </span>
                  )}
                </div>
                
                {task.description && (
                  <p className={`mt-1 text-sm transition-colors duration-200 ${
                    task.completed ? "text-gray-400" : "text-gray-600 dark:text-gray-400"
                  }`}>
                    {task.description}
                  </p>
                )}
                
                <div className="flex items-center gap-4 mt-3 text-xs text-gray-400 dark:text-gray-500">
                  <span className="flex items-center gap-1">
                    <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                    </svg>
                    {formatDate(task.created_at)}
                  </span>
                </div>
              </div>

              <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity duration-200">
                <button
                    onClick={() => startEditing(task)}
                    disabled={processingId === task.id || task.completed}
                    className="p-2 text-gray-400 hover:text-blue-600 hover:bg-blue-50 rounded-lg dark:hover:bg-blue-900/20 dark:hover:text-blue-400 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    title="Edit task"
                >
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                </button>
                <button
                    onClick={() => deleteTask(task.id)}
                    disabled={processingId === task.id}
                    className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg dark:hover:bg-red-900/20 dark:hover:text-red-400 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                    title="Delete task"
                >
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                </button>
              </div>
            </div>
          )}
        </li>
      ))}
    </ul>
  );
}
