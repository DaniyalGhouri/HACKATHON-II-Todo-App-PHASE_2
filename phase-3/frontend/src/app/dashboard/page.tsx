"use client";

import { useEffect, useState, useCallback } from "react";
import { useSession } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import { TaskForm } from "@/components/task-form";
import { TaskList } from "@/components/task-list";
import { fetchWithAuth } from "@/lib/api-client";
import { authClient } from "@/lib/auth-client";
import Link from "next/link";

export default function DashboardPage() {
  const { data: session, isPending, error } = useSession();
  const user = session?.user;
  const router = useRouter();
  const [tasks, setTasks] = useState([]);
  const [loadingTasks, setLoadingTasks] = useState(false);

  // Fetch tasks
  const fetchTasks = useCallback(async () => {
    if (!user) return;
    setLoadingTasks(true);
    try {
      const res = await fetchWithAuth(`/api/tasks`);
      if (res.ok) {
        const data = await res.json();
        setTasks(data);
      }
    } catch (err) {
      console.error("Failed to fetch tasks", err);
    } finally {
      setLoadingTasks(false);
    }
  }, [user]);

  useEffect(() => {
    if (!isPending && !user) {
      router.push("/login");
    }
  }, [user, isPending, router]);

  useEffect(() => {
    if (user) {
      fetchTasks();
    }
  }, [user, fetchTasks]);

  if (isPending || !user) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-black">
        <div className="flex flex-col items-center space-y-4">
          <div className="w-8 h-8 border-4 border-black border-t-transparent rounded-full animate-spin dark:border-white dark:border-t-transparent"></div>
          <p className="text-gray-500 dark:text-gray-400">Loading your workspace...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50/50 dark:bg-black font-sans">
      {/* Header */}
      <header className="sticky top-0 z-10 backdrop-blur-md bg-white/70 dark:bg-zinc-900/70 border-b border-gray-200 dark:border-zinc-800">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center gap-3">
              <div className="h-8 w-8 bg-black dark:bg-white rounded-lg flex items-center justify-center">
                <span className="text-white dark:text-black font-bold text-xl">T</span>
              </div>
              <h1 className="text-xl font-bold text-gray-900 dark:text-white tracking-tight">Todo App</h1>
            </div>
            
            <div className="flex items-center gap-6">
              <Link
                href="/chat"
                className="flex items-center gap-2 text-sm font-bold uppercase tracking-widest text-gray-500 hover:text-black dark:text-zinc-400 dark:hover:text-white transition-all"
              >
                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
                AI Assistant
              </Link>
              <div className="hidden sm:block text-xs font-medium text-gray-400 dark:text-zinc-500">
                {user.email}
              </div>
              <button
                onClick={async () => {
                    await authClient.signOut();
                    router.push("/login");
                }}
                className="text-xs font-bold uppercase tracking-widest text-gray-600 hover:text-black dark:text-zinc-400 dark:hover:text-white transition-colors"
              >
                Sign Out
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="space-y-8">
          <div className="text-center sm:text-left">
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white tracking-tight">
              My Tasks
            </h2>
            <div className="mt-2 flex flex-wrap gap-4 justify-center sm:justify-start">
              <p className="text-gray-600 dark:text-gray-400">
                Manage your daily goals and stay organized.
              </p>
              <div className="flex gap-3 text-sm font-medium">
                <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-blue-50 text-blue-700 dark:bg-blue-900/30 dark:text-blue-400 border border-blue-100 dark:border-blue-800">
                  {tasks.filter((t: any) => !t.completed).length} Pending
                </span>
                <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-green-50 text-green-700 dark:bg-green-900/30 dark:text-green-400 border border-green-100 dark:border-green-800">
                  {tasks.filter((t: any) => t.completed).length} Completed
                </span>
              </div>
            </div>
          </div>

          <TaskForm onTaskCreated={fetchTasks} />
          
          <div className="relative">
            {loadingTasks ? (
               <div className="flex justify-center py-12">
                 <div className="w-6 h-6 border-2 border-gray-300 border-t-black rounded-full animate-spin dark:border-zinc-700 dark:border-t-white"></div>
               </div>
            ) : (
               <TaskList tasks={tasks} onTaskUpdated={fetchTasks} />
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
