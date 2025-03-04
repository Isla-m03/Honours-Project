import React, { useState, useEffect } from "react";
import axios from "axios";

const Forecast = () => {
    const [date, setDate] = useState("");
    const [revenue, setRevenue] = useState("");
    const [forecasts, setForecasts] = useState([]);
    const [editingId, setEditingId] = useState(null);

    useEffect(() => {
        fetchForecasts();
    }, []);

    const fetchForecasts = async () => {
        try {
            const res = await axios.get("http://127.0.0.1:5000/forecast");
            setForecasts(res.data);
        } catch (error) {
            console.error("Error fetching forecasts:", error);
        }
    };

    const updateForecast = async (id) => {
        try {
            await axios.put(`http://127.0.0.1:5000/forecast/${id}`, { date, revenue: parseInt(revenue) });
            setEditingId(null);
            fetchForecasts();
        } catch (error) {
            console.error("Error updating forecast:", error);
        }
    };

    const deleteForecast = async (id) => {
        try {
            await axios.delete(`http://127.0.0.1:5000/forecast/${id}`);
            fetchForecasts();
        } catch (error) {
            console.error("Error deleting forecast:", error);
        }
    };

    return (
        <div>
            <h2>Update Forecast</h2>
            <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
            <input type="number" placeholder="Revenue" value={revenue} onChange={(e) => setRevenue(e.target.value)} />
            {editingId ? <button onClick={() => updateForecast(editingId)}>Update</button> : <button onClick={updateForecast}>Add Forecast</button>}

            <h3>Forecasts</h3>
            {forecasts.map(f => (
                <div key={f.id}>{f.date}: ${f.revenue} <button onClick={() => deleteForecast(f.id)}>🗑</button></div>
            ))}
        </div>
    );
};

export default Forecast;
