"use client";

import { useState } from "react";
import { fetchWithAuth } from "@/lib/api-client";

interface TaskFormProps {
  onTaskCreated: () => void;
}

export function TaskForm({ onTaskCreated }: TaskFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [priority, setPriority] = useState("medium");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isExpanded, setIsExpanded] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const response = await fetchWithAuth(`/api/tasks`, {
        method: "POST",
        body: JSON.stringify({
          title,
          description: description || null,
          due_date: dueDate ? new Date(dueDate).toISOString() : null,
          priority: priority
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || "Failed to create task");
      }

      setTitle("");
      setDescription("");
      setDueDate("");
      setPriority("medium");
      setIsExpanded(false);
      onTaskCreated();
    } catch (err: any) {
        setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mb-8 bg-white dark:bg-zinc-900 rounded-2xl shadow-sm border border-gray-200 dark:border-zinc-800 overflow-hidden transition-all duration-300">
      <form onSubmit={handleSubmit} className="p-5 sm:p-7 space-y-5">
        <div>
          <label htmlFor="title" className="sr-only">
            New Task
          </label>
          <input
            type="text"
            id="title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            onFocus={() => setIsExpanded(true)}
            placeholder="What needs to be done?"
            required
            className="block w-full text-xl font-bold border-0 border-b-2 border-transparent focus:border-black dark:focus:border-white focus:ring-0 bg-transparent px-0 py-2 placeholder-gray-400 dark:placeholder-zinc-600 dark:text-white transition-all duration-200"
          />
        </div>
        
        <div className={`space-y-5 transition-all duration-500 ease-in-out ${isExpanded || title ? 'opacity-100 max-h-[500px] translate-y-0' : 'opacity-0 max-h-0 overflow-hidden -translate-y-4'}`}>
          <div>
            <label htmlFor="description" className="block text-xs font-bold uppercase tracking-widest text-gray-400 dark:text-zinc-500 mb-2 ml-1">
              Description
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Add more context..."
              rows={3}
              className="block w-full resize-none rounded-xl border-gray-100 bg-gray-50 focus:bg-white focus:border-black focus:ring-0 dark:bg-zinc-800 dark:border-zinc-700 dark:text-gray-100 dark:focus:bg-zinc-900 sm:text-sm p-4 transition-all duration-200"
            />
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            <div>
              <label htmlFor="due_date" className="block text-xs font-bold uppercase tracking-widest text-gray-400 dark:text-zinc-500 mb-2 ml-1">
                Due Date
              </label>
              <input
                type="datetime-local"
                id="due_date"
                value={dueDate}
                onChange={(e) => setDueDate(e.target.value)}
                className="block w-full rounded-xl border-gray-100 bg-gray-50 focus:bg-white focus:border-black focus:ring-0 dark:bg-zinc-800 dark:border-zinc-700 dark:text-gray-100 dark:focus:bg-zinc-900 sm:text-sm p-3 transition-all duration-200"
              />
            </div>
            <div>
              <label htmlFor="priority" className="block text-xs font-bold uppercase tracking-widest text-gray-400 dark:text-zinc-500 mb-2 ml-1">
                Priority
              </label>
              <select
                id="priority"
                value={priority}
                onChange={(e) => setPriority(e.target.value)}
                className="block w-full rounded-xl border-gray-100 bg-gray-50 focus:bg-white focus:border-black focus:ring-0 dark:bg-zinc-800 dark:border-zinc-700 dark:text-gray-100 dark:focus:bg-zinc-900 sm:text-sm p-3 transition-all duration-200 appearance-none"
              >
                <option value="low">Low Priority</option>
                <option value="medium">Medium Priority</option>
                <option value="high">High Priority</option>
              </select>
            </div>
          </div>
          
          {error && <p className="text-red-500 text-sm font-medium bg-red-50 dark:bg-red-900/20 px-4 py-2 rounded-lg">{error}</p>}
          
          <div className="flex justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={() => { setIsExpanded(false); setTitle(""); setDescription(""); setDueDate(""); setPriority("medium"); }}
              className="px-5 py-2.5 text-sm font-bold uppercase tracking-wider text-gray-500 bg-transparent rounded-xl hover:bg-gray-100 dark:text-zinc-400 dark:hover:bg-zinc-800 transition-all duration-200"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="inline-flex items-center px-6 py-2.5 text-sm font-bold uppercase tracking-wider text-white bg-black rounded-xl hover:opacity-90 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-black disabled:opacity-20 dark:bg-white dark:text-black dark:focus:ring-white transition-all duration-200 shadow-lg shadow-black/5"
            >
              {loading ? "Creating..." : "Create Task"}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
