// Prefer same-origin proxy (/backend) so the browser never hits another origin.
const API_URL = (process.env.NEXT_PUBLIC_API_URL || "/backend").replace(/\/$/, "");

export function getApiUrl(path: string = ""): string {
  const p = path.startsWith("/") ? path : `/${path}`;
  return `${API_URL}${p}`;
}

export async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const url = getApiUrl(path);
  let res: Response;
  try {
    res = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...(options?.headers || {}),
      },
    });
  } catch {
    throw new Error(
      "Cannot reach the API. Start the backend first:\n" +
        "  cd resumekeywordchecker/backend\n" +
        "  python -m uvicorn main:app --reload --port 8010\n" +
        "Then refresh this page."
    );
  }

  if (!res.ok) {
    let detail: unknown = res.statusText;
    try {
      const body = await res.json();
      detail = body.detail ?? body;
    } catch {
      /* ignore */
    }
    if (typeof detail === "string") {
      throw new Error(detail);
    }
    throw new Error(JSON.stringify(detail));
  }

  if (res.status === 204) {
    return undefined as T;
  }
  return res.json() as Promise<T>;
}
