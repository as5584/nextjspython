"use client";

import { useCallback, useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";

type Expense = {
  id: number;
  date: string;
  category: string;
  item: string;
  amount: number;
  payment_method: string;
};
type Analytics = {
  total: number;
  by_category: { category: string; amount: number }[];
  by_month: { month: string; amount: number }[];
  highest_category: { category: string; amount: number } | null;
};

export default function HomePage() {
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [categories, setCategories] = useState<string[]>([]);
  const [methods, setMethods] = useState<string[]>([]);
  const [form, setForm] = useState({
    category: "FOOD",
    item: "",
    amount: "",
    payment_method: "Online",
    date: "",
  });
  const [filterCategory, setFilterCategory] = useState("");
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const refresh = useCallback(async () => {
    try {
      setError("");
      const q = filterCategory ? `?category=${encodeURIComponent(filterCategory)}` : "";
      const [meta, list, an] = await Promise.all([
        apiFetch<{ categories: string[]; payment_methods: string[] }>("/expenses/meta"),
        apiFetch<Expense[]>(`/expenses${q}`),
        apiFetch<Analytics>("/expenses/analytics"),
      ]);
      setCategories(meta.categories);
      setMethods(meta.payment_methods);
      setExpenses(list);
      setAnalytics(an);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load expenses");
    }
  }, [filterCategory]);

  useEffect(() => {
    refresh();
  }, [refresh]);

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    setMessage("");
    try {
      await apiFetch("/expenses", {
        method: "POST",
        body: JSON.stringify({
          ...form,
          amount: Number(form.amount),
          date: form.date || null,
        }),
      });
      setForm({ ...form, item: "", amount: "" });
      setMessage("Expense added");
      await refresh();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed");
    }
  }

  return (
    <main>
      <div className="hero">
        <h1>Expense Tracker</h1>
        <p>Log spending and view category analytics.</p>
      </div>
      {error && (
        <div className="error" style={{ whiteSpace: "pre-wrap" }}>
          {error}
        </div>
      )}
      {message && <div className="success">{message}</div>}

      <div className="grid grid-2">
        <div className="card">
          <h3>Add expense</h3>
          <form onSubmit={onSubmit} className="grid" style={{ gap: 10 }}>
            <div>
              <label>Category</label>
              <select
                value={form.category}
                onChange={(e) => setForm({ ...form, category: e.target.value })}
              >
                {categories.map((c) => (
                  <option key={c}>{c}</option>
                ))}
              </select>
            </div>
            <div>
              <label>Item</label>
              <input
                value={form.item}
                onChange={(e) => setForm({ ...form, item: e.target.value })}
                required
              />
            </div>
            <div>
              <label>Amount</label>
              <input
                type="number"
                step="0.01"
                value={form.amount}
                onChange={(e) => setForm({ ...form, amount: e.target.value })}
                required
              />
            </div>
            <div>
              <label>Payment</label>
              <select
                value={form.payment_method}
                onChange={(e) => setForm({ ...form, payment_method: e.target.value })}
              >
                {methods.map((m) => (
                  <option key={m}>{m}</option>
                ))}
              </select>
            </div>
            <div>
              <label>Date</label>
              <input
                type="date"
                value={form.date}
                onChange={(e) => setForm({ ...form, date: e.target.value })}
              />
            </div>
            <button type="submit">Add expense</button>
          </form>
        </div>

        <div className="card">
          <h3>Analytics</h3>
          <p className="stat">₹{analytics?.total?.toFixed(2) ?? "0.00"}</p>
          <p className="muted">Total spent</p>
          {analytics?.highest_category && (
            <p style={{ marginTop: 12 }}>
              Highest: <strong>{analytics.highest_category.category}</strong> (₹
              {analytics.highest_category.amount.toFixed(2)})
            </p>
          )}
          <h4>By category</h4>
          <ul>
            {analytics?.by_category.map((c) => (
              <li key={c.category}>
                {c.category}: ₹{c.amount.toFixed(2)}
              </li>
            ))}
          </ul>
          <h4>By month</h4>
          <ul>
            {analytics?.by_month.map((m) => (
              <li key={m.month}>
                {m.month}: ₹{m.amount.toFixed(2)}
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="card">
        <div className="row">
          <div>
            <label>Filter category</label>
            <select value={filterCategory} onChange={(e) => setFilterCategory(e.target.value)}>
              <option value="">All</option>
              {categories.map((c) => (
                <option key={c}>{c}</option>
              ))}
            </select>
          </div>
        </div>
        <table style={{ marginTop: 12 }}>
          <thead>
            <tr>
              <th>Date</th>
              <th>Category</th>
              <th>Item</th>
              <th>Amount</th>
              <th>Payment</th>
            </tr>
          </thead>
          <tbody>
            {expenses.map((e) => (
              <tr key={e.id}>
                <td>{e.date}</td>
                <td>{e.category}</td>
                <td>{e.item}</td>
                <td>₹{e.amount.toFixed(2)}</td>
                <td>{e.payment_method}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </main>
  );
}
