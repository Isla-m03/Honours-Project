import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import { UserContext } from "../App";

const Forecast = () => {
  const { user } = useContext(UserContext);
  const token = user?.token;

  const [forecasts, setForecasts] = useState([]);
  const [form, setForm] = useState({ date: "", revenue: "" });
  const [editId, setEditId] = useState(null);

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
      if (editId) {
        await axios.put(
          `http://localhost:5000/forecast/${editId}`,
          form,
          { headers: { Authorization: `Bearer ${token}` } }
        );
        setEditId(null);
      } else {
        await axios.post("http://localhost:5000/forecast", form, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }
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

  const handleEdit = (forecast) => {
    setForm({ date: forecast.date, revenue: forecast.revenue });
    setEditId(forecast.id);
  };

  useEffect(() => {
    if (token) fetchForecasts();
  }, [token]);

  return (
    <div style={{ padding: 20 }}>
      <h2>{editId ? "Edit Forecast" : "Add Forecast"}</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="date"
          value={form.date}
          onChange={(e) => setForm({ ...form, date: e.target.value })}
          required
        />
        <input
          type="number"
          value={form.revenue}
          onChange={(e) => setForm({ ...form, revenue: e.target.value })}
          placeholder="Revenue"
          required
        />
        <button type="submit">{editId ? "Update" : "Add"} Forecast</button>
      </form>

      <h3>Forecasts</h3>
      <ul>
        {forecasts.map((f) => (
          <li key={f.id}>
            ID: {f.id} — {f.date} — £{f.revenue}
            <button onClick={() => handleEdit(f)} style={{ marginLeft: 10 }}>Edit</button>
            <button onClick={() => handleDelete(f.id)} style={{ marginLeft: 10 }}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Forecast;

