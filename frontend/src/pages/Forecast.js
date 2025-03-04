import React, { useState, useEffect } from "react";
import axios from "axios";

const Forecast = () => {
    const [date, setDate] = useState("");
    const [revenue, setRevenue] = useState("");
    const [forecasts, setForecasts] = useState([]);

    // Fetch existing forecasts
    useEffect(() => {
        fetchForecasts();
    }, []);

    const fetchForecasts = async () => {
        try {
            const res = await axios.get("http://127.0.0.1:5000/forecast");
            console.log("Fetched Forecasts:", res.data);  // Debugging
            setForecasts(res.data);
        } catch (error) {
            console.error("Error fetching forecasts:", error);
        }
    };

    const addForecast = async () => {
        try {
            const res = await axios.post("http://127.0.0.1:5000/forecast", {
                date,
                revenue: parseInt(revenue)
            });
            console.log("Add Forecast Response:", res.data);  // Debugging
            setDate("");
            setRevenue("");
            fetchForecasts(); // Refresh after adding
        } catch (error) {
            console.error("Error adding forecast:", error.response ? error.response.data : error);
        }
    };

    const deleteForecast = async (id) => {
        console.log("🛑 Attempting to delete forecast with ID:", id); // Debugging
    
        if (!id) {
            console.error("❌ Error: Forecast ID is undefined!");
            return;
        }
    
        try {
            const res = await axios.delete(`http://127.0.0.1:5000/forecast/${id}`);
            console.log("✅ Delete Forecast Response:", res.data);
            fetchForecasts(); // Refresh list after deleting
        } catch (error) {
            console.error("❌ Error deleting forecast:", error.response ? error.response.data : error);
        }
    };
    ;
    

    return (
        <div className="container">
            <h2>Manage Forecasts</h2>
            
            {/* Add Forecast Form */}
            <div className="form">
                <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
                <input type="number" placeholder="Revenue" value={revenue} onChange={(e) => setRevenue(e.target.value)} />
                <button onClick={addForecast}>Add Forecast</button>
            </div>

            {/* Display Forecasts */}
            <h3>Existing Forecasts</h3>
            <table>
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Revenue</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {forecasts.length > 0 ? (
                        forecasts.map((f) => (
                            <tr key={f.id}>
                                <td>{f.date}</td>
                                <td>${f.revenue}</td>
                                <td>
                                    <button onClick={() => deleteForecast(f.id)}>🗑 Delete</button>
                                </td>
                            </tr>
                        ))
                    ) : (
                        <tr>
                            <td colSpan="3">No forecasts found.</td>
                        </tr>
                    )}
                </tbody>

            </table>
        </div>
    );
};

export default Forecast;

