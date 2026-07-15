"use client";

import { useCallback, useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Student = { name: string };
type Summary = { student: string; total_days: number; present: number; percentage: number };

export default function HomePage() {
  const [students, setStudents] = useState<Student[]>([]);
  const [summary, setSummary] = useState<Summary[]>([]);
  const [low, setLow] = useState<Summary[]>([]);
  const [name, setName] = useState("");
  const [date, setDate] = useState("");
  const [marks, setMarks] = useState<Record<string, string>>({});
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const refresh = useCallback(async () => {
    try {
      setError("");
      const [s, sum, lo] = await Promise.all([
        apiFetch<Student[]>("/students"),
        apiFetch<{ students: Summary[] }>("/attendance/summary"),
        apiFetch<{ students: Summary[] }>("/attendance/low?threshold=75"),
      ]);
      setStudents(s);
      setSummary(sum.students);
      setLow(lo.students);
      const init: Record<string, string> = {};
      s.forEach((st) => {
        init[st.name] = marks[st.name] || "P";
      });
      setMarks(init);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load data");
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  async function addStudent(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setMessage("");
    setLoading(true);
    try {
      await apiFetch("/students", {
        method: "POST",
        body: JSON.stringify({ name }),
      });
      setName("");
      setMessage("Student added");
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    } finally {
      setLoading(false);
    }
  }

  async function recordAttendance(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setMessage("");
    setLoading(true);
    try {
      await apiFetch("/attendance/records", {
        method: "POST",
        body: JSON.stringify({
          date: date || null,
          marks: students.map((s) => ({ student: s.name, status: marks[s.name] || "A" })),
        }),
      });
      setMessage("Attendance recorded");
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
        <h1>Attendance Manager</h1>
        <p>Track students, mark attendance, and spot low attendance.</p>
      </div>
      {error && (
        <div className="error" style={{ whiteSpace: "pre-wrap" }}>
          {error}
        </div>
      )}
      {message && <div className="success">{message}</div>}

      <div className="grid grid-2">
        <div className="card">
          <h3>Add Student</h3>
          <form onSubmit={addStudent} className="row">
            <div>
              <label>Name</label>
              <input value={name} onChange={(e) => setName(e.target.value)} required />
            </div>
            <button type="submit" disabled={loading}>Add</button>
          </form>
        </div>

        <div className="card">
          <h3>Record Attendance</h3>
          <form onSubmit={recordAttendance}>
            <label>Date (optional)</label>
            <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
            <div style={{ marginTop: 12 }}>
              {students.length === 0 && <p className="muted">No students yet.</p>}
              {students.map((s) => (
                <div key={s.name} className="row" style={{ marginBottom: 8 }}>
                  <div style={{ flex: 2 }}>{s.name}</div>
                  <select
                    value={marks[s.name] || "P"}
                    onChange={(e) => setMarks({ ...marks, [s.name]: e.target.value })}
                  >
                    <option value="P">Present</option>
                    <option value="A">Absent</option>
                  </select>
                </div>
              ))}
            </div>
            <button type="submit" disabled={loading || !students.length} style={{ marginTop: 12 }}>
              Save attendance
            </button>
          </form>
        </div>
      </div>

      <div className="card">
        <h3>Summary</h3>
        <table>
          <thead>
            <tr>
              <th>Student</th>
              <th>Present</th>
              <th>Days</th>
              <th>%</th>
            </tr>
          </thead>
          <tbody>
            {summary.map((s) => (
              <tr key={s.student}>
                <td>{s.student}</td>
                <td>{s.present}</td>
                <td>{s.total_days}</td>
                <td className={s.percentage < 75 ? "bad" : "ok"}>{s.percentage}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="card">
        <h3>Low attendance (&lt; 75%)</h3>
        {low.length === 0 ? (
          <p className="muted">None</p>
        ) : (
          <ul>
            {low.map((s) => (
              <li key={s.student}>
                {s.student}: {s.percentage}%
              </li>
            ))}
          </ul>
        )}
      </div>
    </main>
  );
}
