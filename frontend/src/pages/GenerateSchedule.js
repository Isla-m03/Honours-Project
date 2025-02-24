import React, { useState } from "react";
import axios from "axios";

const GenerateSchedule = () => {
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [response, setResponse] = useState("");

    const generateSchedule = async () => {
        try {
            const res = await axios.post("http://127.0.0.1:5000/generate_schedule", {
                start_date: startDate,
                end_date: endDate,
            });
            setResponse(res.data.message);
        } catch (error) {
            setResponse("Error generating schedule");
        }
    };

    return (
        <div>
            <h2>Generate Schedule</h2>
            <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
            <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
            <button onClick={generateSchedule}>Generate</button>
            <p>{response}</p>
        </div>
    );
};

export default GenerateSchedule;
