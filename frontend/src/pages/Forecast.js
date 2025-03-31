import React, { useState, useEffect } from "react";
import axios from "axios";

const Forecast = () => {
    const [forecasts, setForecasts] = useState([]);
    const [date, setDate] = useState("");
    const [revenue, setRevenue] = useState("");
    const token = localStorage.getItem("token");

    const fetchForecasts = async () => {
        try {
            const res = await axios.get("http://127.0.0.1:5000/forecast", {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setForecasts(res.data);
        } catch (error) {
            console.error("Error fetching forecasts:", error);
        }
    };

    const addForecast = async () => {
        try {
            await axios.post("http://127.0.0.1:5000/forecast", {
                date,
                revenue: parseInt(revenue)
            }, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            fetchForecasts();
        } catch (error) {
            console.error("Error adding forecast:", error);
        }
    };

    useEffect(() => {
        fetchForecasts();
    }, []);

    return (
        <div>
            <h2>Add Forecast</h2>
            <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
            <input type="number" value={revenue} placeholder="Revenue" onChange={(e) => setRevenue(e.target.value)} />
            <button onClick={addForecast}>Add</button>

            <h3>Forecasts</h3>
            <ul>
                {forecasts.map((f) => (
                    <li key={f.id}>{f.date} - £{f.revenue}</li>
                ))}
            </ul>
        </div>
    );
};

export default Forecast;

