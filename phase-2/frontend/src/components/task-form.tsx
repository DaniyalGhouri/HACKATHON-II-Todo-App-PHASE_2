"use client";

import { useState } from "react";
import { fetchWithAuth } from "@/lib/api-client";
import { useRouter } from "next/navigation";

interface TaskFormProps {
  onTaskCreated: () => void;
}

export function TaskForm({ onTaskCreated }: TaskFormProps) {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
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
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        throw new Error(data.detail || "Failed to create task");
      }

      setTitle("");
      setDescription("");
      setIsExpanded(false);
      onTaskCreated();
    } catch (err: any) {
        setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="mb-8 bg-white dark:bg-zinc-900 rounded-xl shadow-sm border border-gray-200 dark:border-zinc-800 overflow-hidden transition-all duration-200">
      <form onSubmit={handleSubmit} className="p-4 sm:p-6 space-y-4">
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
            className="block w-full text-lg font-medium border-0 border-b-2 border-transparent focus:border-black dark:focus:border-white focus:ring-0 bg-transparent px-0 py-2 placeholder-gray-400 dark:text-white transition-colors"
          />
        </div>
        
        <div className={`space-y-4 transition-all duration-300 ease-in-out ${isExpanded || title ? 'opacity-100 max-h-40' : 'opacity-0 max-h-0 overflow-hidden'}`}>
          <div>
            <label htmlFor="description" className="sr-only">
              Description (Optional)
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Add details (optional)"
              rows={2}
              className="block w-full resize-none rounded-lg border-gray-200 bg-gray-50 focus:bg-white focus:border-black focus:ring-1 focus:ring-black dark:bg-zinc-800 dark:border-zinc-700 dark:text-white dark:focus:bg-zinc-800 sm:text-sm p-3 transition-colors"
            />
          </div>
          
          {error && <p className="text-red-500 text-sm bg-red-50 dark:bg-red-900/20 p-2 rounded">{error}</p>}
          
          <div className="flex justify-end gap-3 pt-2">
            <button
              type="button"
              onClick={() => { setIsExpanded(false); setTitle(""); setDescription(""); }}
              className="px-4 py-2 text-sm font-medium text-gray-600 bg-gray-100 rounded-lg hover:bg-gray-200 dark:text-gray-300 dark:bg-zinc-800 dark:hover:bg-zinc-700 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="inline-flex items-center px-4 py-2 text-sm font-medium text-white bg-black rounded-lg hover:bg-zinc-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-black disabled:opacity-50 dark:bg-white dark:text-black dark:hover:bg-zinc-200 transition-colors"
            >
              {loading ? "Adding..." : "Add Task"}
            </button>
          </div>
        </div>
      </form>
    </div>
  );
}
