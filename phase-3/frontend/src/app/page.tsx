"use client";

import { authClient, useSession, signOut } from "@/lib/auth-client"; // Import authClient and its hooks
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function Home() {
  const { data: session, isPending: loading } = useSession(); 
  const user = session?.user;
  const router = useRouter();

  useEffect(() => {
    if (user && !loading) {
      router.push("/dashboard");
    }
  }, [user, loading, router]);

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen">Loading...</div>;
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-zinc-50 dark:bg-black">
      <div className="max-w-2xl text-center space-y-8">
        <h1 className="text-4xl font-bold tracking-tight text-gray-900 dark:text-white sm:text-6xl">
          Phase II Todo App
        </h1>
        <p className="text-lg leading-8 text-gray-600 dark:text-gray-400">
          A secure, multi-user todo application powered by Next.js, FastAPI, and Better Auth.
        </p>
        <div className="flex items-center justify-center gap-x-6">
          {user ? (
            <div className="text-center space-y-4">
              <p className="text-xl">Welcome back, {user.email}</p>
              {/* Link to Dashboard would go here */}
              <button 
                onClick={async () => {
                    await authClient.signOut(); // Use authClient.signOut()
                    router.push("/login"); // Redirect to login page after sign out
                }}
                className="rounded-md bg-red-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-red-500"
              >
                Sign Out
              </button>
            </div>
          ) : (
            <>
              <Link
                href="/login"
                className="rounded-md bg-black px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-gray-800 dark:bg-white dark:text-black dark:hover:bg-gray-200"
              >
                Log In
              </Link>
              <Link
                href="/signup"
                className="text-sm font-semibold leading-6 text-gray-900 dark:text-white"
              >
                Sign Up <span aria-hidden="true">→</span>
              </Link>
            </>
          )}
        </div>
      </div>
    </div>
  );
}