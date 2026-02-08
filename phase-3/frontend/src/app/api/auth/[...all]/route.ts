import { auth } from "@/lib/auth"; // Import from server-side auth config
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);