"use client";

import { useState } from "react";
import { apiFetch } from "@/lib/api";

type Result = {
  checks: {
    has_uppercase: boolean;
    has_lowercase: boolean;
    has_numbers: boolean;
    has_symbols: boolean;
    min_length: boolean;
  };
  score: number;
  max_score: number;
  percentage: number;
  strength: string;
};

const LABELS: Record<string, string> = {
  has_uppercase: "Uppercase letters (A-Z)",
  has_lowercase: "Lowercase letters (a-z)",
  has_numbers: "Numbers (0-9)",
  has_symbols: "Symbols (!@#$...)",
  min_length: "At least 8 characters",
};

export default function HomePage() {
  const [password, setPassword] = useState("");
  const [result, setResult] = useState<Result | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function check(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await apiFetch<Result>("/password/check", {
        method: "POST",
        body: JSON.stringify({ password }),
      });
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main>
      <div className="hero">
        <h1>Password Strength Checker</h1>
        <p>Check password criteria and strength score.</p>
      </div>
      {error && (
        <div className="error" style={{ whiteSpace: "pre-wrap" }}>
          {error}
        </div>
      )}

      <div className="card">
        <form onSubmit={check} className="row">
          <div style={{ flex: 3 }}>
            <label>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" disabled={loading}>
            Check
          </button>
        </form>
      </div>

      {result && (
        <div className="card">
          <p className="stat">{result.strength}</p>
          <p className="muted">
            Score {result.score}/{result.max_score} · {result.percentage}%
          </p>
          <div style={{ marginTop: 16 }}>
            {Object.entries(result.checks).map(([key, ok]) => (
              <div key={key} style={{ marginBottom: 8 }}>
                <span className={ok ? "ok" : "bad"}>{ok ? "PASS" : "FAIL"}</span>{" "}
                {LABELS[key] || key}
              </div>
            ))}
          </div>
        </div>
      )}
    </main>
  );
}
