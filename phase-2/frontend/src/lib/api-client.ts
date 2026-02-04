const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type FetchOptions = RequestInit & {
  headers?: Record<string, string>;
};

export async function fetchWithAuth(endpoint: string, options: FetchOptions = {}) {
  const url = `${API_URL}${endpoint}`;

  const defaultHeaders: Record<string, string> = {
    "Content-Type": "application/json",
  };

  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
    credentials: "include", // Send cookies (including better-auth.session_token)
  };

  const response = await fetch(url, config);

  if (response.status === 401) {
    if (typeof window !== "undefined" && !window.location.pathname.startsWith("/login")) {
         window.location.href = "/login";
    }
  }

  return response;
}
