"use client";

import { useState } from "react";
import { fetchWithAuth } from "@/lib/api-client";

interface Task {
  id: number; 
  title: string;
  description?: string;
  completed: boolean; 
  due_date?: string;
  priority: "low" | "medium" | "high";
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
  const [editDueDate, setEditDueDate] = useState("");
  const [editPriority, setEditPriority] = useState<"low" | "medium" | "high">("medium");

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString(undefined, {
      month: "short",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    });
  };

  const startEditing = (task: Task) => {
    setEditingId(task.id);
    setEditTitle(task.title);
    setEditDescription(task.description || "");
    setEditDueDate(task.due_date ? new Date(task.due_date).toISOString().slice(0, 16) : "");
    setEditPriority(task.priority);
  };

  const cancelEditing = () => {
    setEditingId(null);
    setEditTitle("");
    setEditDescription("");
    setEditDueDate("");
  };

  const saveTask = async (taskId: number) => {
    if (!editTitle.trim()) return;
    
    setProcessingId(taskId);
    try {
      await fetchWithAuth(`/api/tasks/${taskId}`, {
        method: "PATCH",
        body: JSON.stringify({ 
          title: editTitle,
          description: editDescription || null,
          due_date: editDueDate ? new Date(editDueDate).toISOString() : null,
          priority: editPriority
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

  const priorityColors = {
    low: "bg-blue-50 text-blue-600 dark:bg-blue-500/10 dark:text-blue-400 border border-blue-100 dark:border-blue-500/20",
    medium: "bg-amber-50 text-amber-600 dark:bg-amber-500/10 dark:text-amber-400 border border-amber-100 dark:border-amber-500/20",
    high: "bg-rose-50 text-rose-600 dark:bg-rose-500/10 dark:text-rose-400 border border-rose-100 dark:border-rose-500/20",
  };

  if (tasks.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-20 px-4 text-center bg-white dark:bg-zinc-900/50 rounded-2xl border border-dashed border-gray-200 dark:border-zinc-800">
        <div className="bg-gray-50 dark:bg-zinc-900 p-5 rounded-2xl mb-6">
          <svg className="w-10 h-10 text-gray-300 dark:text-zinc-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
        </div>
        <h3 className="text-xl font-bold text-gray-900 dark:text-white">A fresh start</h3>
        <p className="mt-2 text-gray-500 dark:text-zinc-500 max-w-sm text-sm">
          No tasks found for your workspace. Use the form above to add your first goal.
        </p>
      </div>
    );
  }

  return (
    <ul className="space-y-4">
      {tasks.map((task) => (
        <li
          key={task.id}
          className={`group relative overflow-hidden bg-white dark:bg-zinc-900 rounded-2xl border transition-all duration-300 hover:shadow-xl hover:shadow-black/5 dark:hover:shadow-none ${
            task.completed 
              ? "border-gray-100 dark:border-zinc-800 bg-gray-50/50 dark:bg-zinc-900/40 opacity-70" 
              : "border-gray-200 dark:border-zinc-800 hover:border-black/10 dark:hover:border-white/10"
          }`}
        >
          {editingId === task.id ? (
            <div className="p-5 space-y-4 animate-in fade-in slide-in-from-top-2 duration-200">
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                className="w-full px-4 py-2.5 bg-gray-50 dark:bg-zinc-800 border-0 focus:ring-2 focus:ring-black dark:focus:ring-white rounded-xl dark:text-white font-bold"
                placeholder="Task Title"
                autoFocus
              />
              <textarea
                value={editDescription}
                onChange={(e) => setEditDescription(e.target.value)}
                className="w-full px-4 py-2.5 bg-gray-50 dark:bg-zinc-800 border-0 focus:ring-2 focus:ring-black dark:focus:ring-white rounded-xl dark:text-white resize-none text-sm"
                placeholder="Description"
                rows={2}
              />
              <div className="grid grid-cols-2 gap-4">
                <input
                  type="datetime-local"
                  value={editDueDate}
                  onChange={(e) => setEditDueDate(e.target.value)}
                  className="px-4 py-2 bg-gray-50 dark:bg-zinc-800 border-0 focus:ring-2 focus:ring-black dark:focus:ring-white rounded-xl dark:text-white text-xs"
                />
                <select
                  value={editPriority}
                  onChange={(e) => setEditPriority(e.target.value as any)}
                  className="px-4 py-2 bg-gray-50 dark:bg-zinc-800 border-0 focus:ring-2 focus:ring-black dark:focus:ring-white rounded-xl dark:text-white text-xs appearance-none"
                >
                  <option value="low">Low</option>
                  <option value="medium">Medium</option>
                  <option value="high">High</option>
                </select>
              </div>
              <div className="flex gap-2 justify-end pt-2">
                <button
                  onClick={cancelEditing}
                  className="px-4 py-2 text-xs font-bold uppercase tracking-widest text-gray-500 bg-transparent rounded-xl hover:bg-gray-100 dark:text-zinc-400 dark:hover:bg-zinc-800 transition-all"
                >
                  Cancel
                </button>
                <button
                  onClick={() => saveTask(task.id)}
                  disabled={processingId === task.id}
                  className="px-4 py-2 text-xs font-bold uppercase tracking-widest text-white bg-black rounded-xl hover:opacity-90 dark:bg-white dark:text-black transition-all"
                >
                  Save Changes
                </button>
              </div>
            </div>
          ) : (
            <div className="flex items-start p-5 sm:p-6 gap-5">
              <div className="pt-1">
                <div className="relative flex items-center justify-center w-6 h-6">
                    <input
                    type="checkbox"
                    checked={task.completed}
                    onChange={() => toggleCompletion(task)}
                    disabled={processingId === task.id}
                    className="peer absolute opacity-0 w-full h-full cursor-pointer z-10"
                    />
                    <div className={`w-6 h-6 rounded-lg border-2 transition-all duration-200 flex items-center justify-center ${
                        task.completed 
                        ? 'bg-black border-black dark:bg-white dark:border-white' 
                        : 'border-gray-200 dark:border-zinc-700 hover:border-black dark:hover:border-white'
                    }`}>
                        {task.completed && (
                            <svg className="w-4 h-4 text-white dark:text-black" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                            </svg>
                        )}
                    </div>
                </div>
              </div>
              
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-3 flex-wrap mb-1.5">
                  <h3 className={`text-lg font-bold tracking-tight transition-all duration-300 ${
                    task.completed 
                      ? "text-gray-400 line-through decoration-gray-300" 
                      : "text-gray-900 dark:text-white"
                  }`}>
                    {task.title}
                  </h3>
                  <span className={`inline-flex items-center px-2 py-0.5 rounded-lg text-[10px] font-black uppercase tracking-tighter ${priorityColors[task.priority]}`}>
                    {task.priority}
                  </span>
                </div>
                
                {task.description && (
                  <p className={`text-sm leading-relaxed transition-colors duration-300 ${
                    task.completed ? "text-gray-300 dark:text-zinc-600" : "text-gray-500 dark:text-zinc-400"
                  }`}>
                    {task.description}
                  </p>
                )}
                
                <div className="flex items-center gap-5 mt-4 text-[10px] font-bold uppercase tracking-widest text-gray-400 dark:text-zinc-500">
                  <span className="flex items-center gap-1.5">
                    <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                    </svg>
                    {formatDate(task.created_at)}
                  </span>
                  {task.due_date && (
                    <span className={`flex items-center gap-1.5 ${new Date(task.due_date) < new Date() && !task.completed ? 'text-rose-500 animate-pulse' : ''}`}>
                      <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      Due {formatDate(task.due_date)}
                    </span>
                  )}
                </div>
              </div>

              <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-all duration-300">
                <button
                    onClick={() => startEditing(task)}
                    disabled={processingId === task.id || task.completed}
                    className="p-2.5 text-gray-400 hover:text-black hover:bg-gray-100 dark:hover:bg-zinc-800 dark:hover:text-white rounded-xl transition-all disabled:opacity-20"
                    title="Edit task"
                >
                    <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" />
                    </svg>
                </button>
                <button
                    onClick={() => deleteTask(task.id)}
                    disabled={processingId === task.id}
                    className="p-2.5 text-gray-400 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-900/20 dark:hover:text-rose-400 rounded-xl transition-all disabled:opacity-20"
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
