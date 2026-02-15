const API_URL = "/backend";

type FetchOptions = RequestInit & {
  headers?: Record<string, string>;
};

function getCookie(name: string) {
  if (typeof document === "undefined") return null;
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop()?.split(";").shift();
  return null;
}

export async function fetchWithAuth(endpoint: string, options: FetchOptions = {}) {
  const url = `${API_URL}${endpoint}`;

  const token = getCookie("better-auth.session_token");

  const defaultHeaders: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (token) {
    defaultHeaders["Authorization"] = `Bearer ${token}`;
  }

  const config: RequestInit = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
    credentials: "include", // Send cookies anyway
  };

  const response = await fetch(url, config);

  if (response.status === 401) {
    if (typeof window !== "undefined" && !window.location.pathname.startsWith("/login")) {
         window.location.href = "/login";
    }
  }

  return response;
}