import React, { useState, useEffect } from "react";
import axios from "axios";

const HolidayRequests = () => {
    const [employeeId, setEmployeeId] = useState("");
    const [date, setDate] = useState("");
    const [requests, setRequests] = useState([]);

    const submitRequest = async () => {
        try {
            await axios.post("http://127.0.0.1:5000/holiday_requests", {
                employee_id: parseInt(employeeId),
                date,
            });
            setEmployeeId("");
            setDate("");
            fetchRequests(); // refresh list
        } catch (error) {
            console.error("Error submitting request:", error);
        }
    };

    const fetchRequests = async () => {
        try {
            const res = await axios.get("http://127.0.0.1:5000/holiday_requests");
            setRequests(res.data);
        } catch (error) {
            console.error("Error fetching requests:", error);
        }
    };

    useEffect(() => {
        fetchRequests();
    }, []);

    return (
        <div>
            <h2>Submit Holiday Request</h2>
            <input
                type="number"
                placeholder="Employee ID"
                value={employeeId}
                onChange={(e) => setEmployeeId(e.target.value)}
            />
            <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
            />
            <button onClick={submitRequest}>Submit</button>

            <h3>Current Holiday Requests</h3>
            <table border="1">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Employee ID</th>
                        <th>Date</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {requests.map((r) => (
                        <tr key={r.id}>
                            <td>{r.id}</td>
                            <td>{r.employee_id}</td>
                            <td>{r.date}</td>
                            <td>{r.status}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default HolidayRequests;
