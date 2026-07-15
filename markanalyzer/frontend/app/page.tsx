"use client";

import { useCallback, useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Student = {
  roll: number;
  name: string;
  math: number;
  science: number;
  english: number;
  average: number;
  status: string;
};
type Analysis = {
  students: Student[];
  class_average: number;
  topper: Student | null;
  failed: Student[];
};

export default function HomePage() {
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [form, setForm] = useState({
    roll: "",
    name: "",
    math: "",
    science: "",
    english: "",
  });
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const refresh = useCallback(async () => {
    try {
      setError("");
      setAnalysis(await apiFetch<Analysis>("/marks/analysis"));
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load analysis");
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  async function addStudent(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setMessage("");
    try {
      await apiFetch("/marks/students", {
        method: "POST",
        body: JSON.stringify({
          roll: Number(form.roll),
          name: form.name,
          math: Number(form.math),
          science: Number(form.science),
          english: Number(form.english),
        }),
      });
      setForm({ roll: "", name: "", math: "", science: "", english: "" });
      setMessage("Student added");
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  }

  return (
    <main>
      <div className="hero">
        <h1>Marks Analyzer</h1>
        <p>Student averages, toppers, and fail list.</p>
      </div>
      {error && (
        <div className="error" style={{ whiteSpace: "pre-wrap" }}>
          {error}
        </div>
      )}
      {message && <div className="success">{message}</div>}

      <div className="grid grid-2">
        <div className="card">
          <h3>Add student</h3>
          <form onSubmit={addStudent} className="grid" style={{ gap: 10 }}>
            {(["roll", "name", "math", "science", "english"] as const).map((k) => (
              <div key={k}>
                <label>{k}</label>
                <input
                  value={form[k]}
                  onChange={(e) => setForm({ ...form, [k]: e.target.value })}
                  required
                  type={k === "name" ? "text" : "number"}
                />
              </div>
            ))}
            <button type="submit">Add</button>
          </form>
        </div>
        <div className="card">
          <h3>Class stats</h3>
          <p className="stat">{analysis?.class_average?.toFixed(2) ?? "0"}</p>
          <p className="muted">Class average</p>
          {analysis?.topper && (
            <p style={{ marginTop: 12 }}>
              Topper: <strong>{analysis.topper.name}</strong> (Roll {analysis.topper.roll}) —{" "}
              {analysis.topper.average}
            </p>
          )}
          <h4>Failed</h4>
          {analysis?.failed?.length ? (
            <ul>
              {analysis.failed.map((s) => (
                <li key={s.roll}>
                  {s.name} (Roll {s.roll})
                </li>
              ))}
            </ul>
          ) : (
            <p className="muted">No failures</p>
          )}
        </div>
      </div>

      <div className="card">
        <h3>Students</h3>
        <table>
          <thead>
            <tr>
              <th>Roll</th>
              <th>Name</th>
              <th>Math</th>
              <th>Science</th>
              <th>English</th>
              <th>Avg</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {analysis?.students.map((s) => (
              <tr key={s.roll}>
                <td>{s.roll}</td>
                <td>{s.name}</td>
                <td>{s.math}</td>
                <td>{s.science}</td>
                <td>{s.english}</td>
                <td>{s.average}</td>
                <td className={s.status === "Pass" ? "ok" : "bad"}>{s.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
