import React, { useState, useEffect } from "react";
import axios from "axios";

const Forecast = () => {
  const [date, setDate] = useState("");
  const [revenue, setRevenue] = useState("");
  const [forecasts, setForecasts] = useState([]);

  const token = localStorage.getItem("token");
  const headers = { Authorization: `Bearer ${token}` };

  const fetchForecasts = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:5000/forecast", { headers });
      setForecasts(res.data);
    } catch (error) {
      console.error("Error fetching forecasts:", error);
    }
  };

  const addForecast = async () => {
    try {
      await axios.post(
        "http://127.0.0.1:5000/forecast",
        { date, revenue: parseInt(revenue) },
        { headers }
      );
      setDate("");
      setRevenue("");
      fetchForecasts();
    } catch (error) {
      console.error("Error adding forecast:", error);
    }
  };

  const deleteForecast = async (id) => {
    try {
      await axios.delete(`http://127.0.0.1:5000/forecast/${id}`, { headers });
      fetchForecasts();
    } catch (error) {
      console.error("Error deleting forecast:", error);
    }
  };

  useEffect(() => {
    fetchForecasts();
  }, []);

  return (
    <div>
      <h2>Add Forecast</h2>
      <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
      <input
        type="number"
        placeholder="Revenue"
        value={revenue}
        onChange={(e) => setRevenue(e.target.value)}
      />
      <button onClick={addForecast}>Add Forecast</button>

      <h3>Forecasts</h3>
      <table border="1">
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
              <td>{f.revenue}</td>
              <td>
                <button onClick={() => deleteForecast(f.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Forecast;


