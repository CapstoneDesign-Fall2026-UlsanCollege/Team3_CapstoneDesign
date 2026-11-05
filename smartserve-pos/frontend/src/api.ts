export const API = import.meta.env.PROD ? "" : "http://localhost:8000";
export type AccountSession = { authenticated: boolean; challenge?: string | null; csrf_token?: string; store_id?: string | null; user?: { id: string; email: string; name: string; role: "platform_admin" | "owner" | "cashier" }; businesses?: { id: string; name: string; role: string }[] };

export async function apiFetch(input: RequestInfo | URL, options: RequestInit = {}) {
  const method = (options.method || "GET").toUpperCase();
  const headers = new Headers(options.headers);
  if (!["GET", "HEAD", "OPTIONS"].includes(method) && !String(input).endsWith("/auth/login") && !String(input).endsWith("/auth/activate")) {
    const session = await fetch(`${API}/auth/session`, { credentials: "include", cache: "no-store" });
    if (session.ok) {
      const data: AccountSession = await session.json();
      if (data.csrf_token) headers.set("X-CSRF-Token", data.csrf_token);
    }
  }
  const response = await fetch(input, { ...options, headers, credentials: "include", cache: "no-store" });
  if (response.status === 401 && !String(input).includes("/auth/")) window.dispatchEvent(new Event("smartserve:session-expired"));
  return response;
}

export async function apiRequest<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await apiFetch(`${API}${path}`, options);
  const data = await response.json();
  if (!response.ok) throw new Error(typeof data.detail === "string" ? data.detail : "Check the fields and try again.");
  return data as T;
}

export const jsonBody = (data: unknown): RequestInit => ({ method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(data) });
