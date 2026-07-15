"use client";

import { useCallback, useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Entry = {
  id: number;
  original_url: string;
  short_url: string;
  created_at: string;
};

export default function HomePage() {
  const [url, setUrl] = useState("");
  const [history, setHistory] = useState<Entry[]>([]);
  const [latest, setLatest] = useState<Entry | null>(null);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const refresh = useCallback(async () => {
    try {
      setError("");
      setHistory(await apiFetch<Entry[]>("/urls"));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load history");
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  async function shorten(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setMessage("");
    setLoading(true);
    try {
      const res = await apiFetch<{ entry: Entry }>("/urls/shorten", {
        method: "POST",
        body: JSON.stringify({ url }),
      });
      setLatest(res.entry);
      setUrl("");
      setMessage("URL shortened");
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <div className="hero">
        <h1>URL Shortener</h1>
        <p>Shorten links with TinyURL and keep history.</p>
      </div>
      {error && (
        <div className="error" style={{ whiteSpace: "pre-wrap" }}>
          {error}
        </div>
      )}
      {message && <div className="success">{message}</div>}

      <div className="card">
        <form onSubmit={shorten} className="row">
          <div style={{ flex: 4 }}>
            <label>Long URL</label>
            <input
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              placeholder="https://example.com/very/long/path"
              required
            />
          </div>
          <button type="submit" disabled={loading}>
            Shorten
          </button>
        </form>
        {latest && (
          <p style={{ marginTop: 16 }}>
            Short link:{" "}
            <a href={latest.short_url} target="_blank" rel="noreferrer" className="ok">
              {latest.short_url}
            </a>
          </p>
        )}
      </div>

      <div className="card">
        <h3>History</h3>
        {history.length === 0 ? (
          <p className="muted">No URLs yet.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Created</th>
                <th>Original</th>
                <th>Short</th>
              </tr>
            </thead>
            <tbody>
              {history.map((h) => (
                <tr key={h.id}>
                  <td>{h.id}</td>
                  <td>{h.created_at}</td>
                  <td style={{ maxWidth: 240, overflow: "hidden", textOverflow: "ellipsis" }}>
                    {h.original_url}
                  </td>
                  <td>
                    <a href={h.short_url} target="_blank" rel="noreferrer">
                      {h.short_url}
                    </a>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </main>
  );
}
