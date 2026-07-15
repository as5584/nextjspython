"use client";

import { useState } from "react";
import { apiFetch } from "@/lib/api";

type Match = {
  resume_keywords: string[];
  job_keywords: string[];
  matched: string[];
  missing: string[];
  extra: string[];
  match_count: number;
  total_job: number;
  percentage: number;
};

export default function HomePage() {
  const [resumeText, setResumeText] = useState("");
  const [jobText, setJobText] = useState("");
  const [result, setResult] = useState<Match | null>(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function match(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const res = await apiFetch<Match>("/resume/match", {
        method: "POST",
        body: JSON.stringify({ resume_text: resumeText, job_text: jobText }),
      });
      setResult(res);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    } finally {
      setLoading(false);
    }
  }

  async function matchFiles() {
    setError("");
    setLoading(true);
    try {
      const res = await apiFetch<Match>("/resume/match-files", { method: "POST" });
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
        <h1>Resume Keyword Checker</h1>
        <p>Compare resume text against a job description.</p>
      </div>
      {error && (
        <div className="error" style={{ whiteSpace: "pre-wrap" }}>
          {error}
        </div>
      )}

      <div className="card">
        <form onSubmit={match} className="grid grid-2">
          <div>
            <label>Resume text</label>
            <textarea value={resumeText} onChange={(e) => setResumeText(e.target.value)} required />
          </div>
          <div>
            <label>Job description</label>
            <textarea value={jobText} onChange={(e) => setJobText(e.target.value)} required />
          </div>
          <div className="row">
            <button type="submit" disabled={loading}>
              Check match
            </button>
            <button type="button" className="secondary" onClick={matchFiles} disabled={loading}>
              Use default files
            </button>
          </div>
        </form>
      </div>

      {result && (
        <div className="card">
          <p className="stat">{result.percentage}%</p>
          <p className="muted">
            Matched {result.match_count}/{result.total_job} job keywords
          </p>
          <h4>Matched</h4>
          <p>{result.matched.join(", ") || "None"}</p>
          <h4>Missing from resume</h4>
          <p className="bad">{result.missing.join(", ") || "None"}</p>
          <h4>Extra in resume</h4>
          <p className="muted">{result.extra.join(", ") || "None"}</p>
        </div>
      )}
    </main>
  );
}
