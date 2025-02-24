import React, { useState } from "react";
import axios from "axios";

const HolidayRequests = () => {
    const [employeeId, setEmployeeId] = useState("");
    const [date, setDate] = useState("");
    const [response, setResponse] = useState("");

    const requestHoliday = async () => {
        try {
            const res = await axios.post("http://127.0.0.1:5000/holiday_requests", {
                employee_id: parseInt(employeeId),
                date,
            });
            setResponse(res.data.message);
        } catch (error) {
            setResponse("Error requesting holiday");
        }
    };

    return (
        <div>
            <h2>Request Holiday</h2>
            <input type="number" placeholder="Employee ID" value={employeeId} onChange={(e) => setEmployeeId(e.target.value)} />
            <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
            <button onClick={requestHoliday}>Request</button>
            <p>{response}</p>
        </div>
    );
};

export default HolidayRequests;
