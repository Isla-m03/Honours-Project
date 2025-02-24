import React, { useState } from "react";
import axios from "axios";

const Forecast = () => {
    const [date, setDate] = useState("");
    const [revenue, setRevenue] = useState("");
    const [response, setResponse] = useState("");

    const updateForecast = async () => {
        try {
            const res = await axios.post("http://127.0.0.1:5000/forecast", {
                date,
                revenue: parseInt(revenue),
            });
            setResponse(res.data.message);
        } catch (error) {
            setResponse("Error updating forecast");
        }
    };

    return (
        <div>
            <h2>Update Forecast</h2>
            <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
            <input type="number" placeholder="Revenue" value={revenue} onChange={(e) => setRevenue(e.target.value)} />
            <button onClick={updateForecast}>Update</button>
            <p>{response}</p>
        </div>
    );
};

export default Forecast;
