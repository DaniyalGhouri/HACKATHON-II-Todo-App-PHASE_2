"use client";
import { createAuthClient } from "better-auth/react";

/**
 * This is the client-side entry point for Better Auth.
 * We are exporting the reactive hooks directly from the client.
 * These hooks can be used in any client component to get auth state.
 */
export const authClient = createAuthClient({
    baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || "http://localhost:3000" 
});

// Re-export hooks if needed, but the authClient instance directly exposes signIn/signUp
export const { useSession, useUser, signIn, signOut } = authClient;