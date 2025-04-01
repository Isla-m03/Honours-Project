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
      const payload = {
        date: form.date,
        revenue: parseInt(form.revenue),
      };
      await axios.post("http://localhost:5000/forecast", payload, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setForm({ date: "", revenue: "" });
      fetchForecasts();
    } catch (err) {
      console.error("❌ Forecast Submit Error:", err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/forecast/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchForecasts();
    } catch (err) {
      console.error("❌ Forecast Delete Error:", err);
    }
  };

  useEffect(() => {
    if (token) fetchForecasts();
  }, [token]);

  return (
    <div style={{ padding: "20px" }}>
      <h2>Add Forecast</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <input
          type="date"
          value={form.date}
          onChange={(e) => setForm({ ...form, date: e.target.value })}
          required
        />
        <input
          type="number"
          placeholder="Revenue"
          value={form.revenue}
          onChange={(e) => setForm({ ...form, revenue: e.target.value })}
          required
        />
        <button type="submit">Add Forecast</button>
      </form>

      <h3>Existing Forecasts</h3>
      <table border="1" cellPadding="8" style={{ width: "100%" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Date</th>
            <th>Revenue</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {forecasts.map((f) => (
            <tr key={f.id}>
              <td>{f.id}</td>
              <td>{f.date}</td>
              <td>£{f.revenue}</td>
              <td>
                <button onClick={() => handleDelete(f.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Forecast;
