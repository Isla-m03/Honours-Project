import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import { UserContext } from "../App";

const Forecast = () => {
  const { user } = useContext(UserContext);
  const token = user?.token;

  const [forecasts, setForecasts] = useState([]);
  const [form, setForm] = useState({ date: "", revenue: "" });

  const fetchForecasts = async () => {
    try {
      const res = await axios.get("http://localhost:5000/forecast", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setForecasts(res.data);
    } catch (err) {
      console.error("❌ Forecast Fetch Error:", err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:5000/forecast", form, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setForm({ date: "", revenue: "" });
      fetchForecasts();
    } catch (err) {
      console.error("❌ Forecast Submit Error:", err);
    }
  };

  useEffect(() => {
    if (token) fetchForecasts();
  }, [token]);

  return (
    <div style={{ padding: 20 }}>
      <h2>Add Forecast</h2>
      <form onSubmit={handleSubmit}>
        <input type="date" value={form.date} onChange={(e) => setForm({ ...form, date: e.target.value })} required />
        <input type="number" value={form.revenue} onChange={(e) => setForm({ ...form, revenue: e.target.value })} placeholder="Revenue" required />
        <button type="submit">Add Forecast</button>
      </form>

      <h3>Forecasts</h3>
      <ul>
        {forecasts.map(f => (
          <li key={f.id}>{f.date} - £{f.revenue}</li>
        ))}
      </ul>
    </div>
  );
};

export default Forecast;
