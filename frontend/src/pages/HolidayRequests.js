import React, { useState, useEffect } from "react";
import axios from "axios";

const HolidayRequests = () => {
    const [employeeId, setEmployeeId] = useState("");
    const [date, setDate] = useState("");
    const [requests, setRequests] = useState([]);
    const [filter, setFilter] = useState("All");

    const token = localStorage.getItem("token");
    const headers = { Authorization: `Bearer ${token}` };

    const submitRequest = async () => {
        try {
            await axios.post(
                "http://127.0.0.1:5000/holiday_requests",
                { employee_id: parseInt(employeeId), date },
                { headers }
            );
            setEmployeeId("");
            setDate("");
            fetchRequests();
        } catch (error) {
            console.error("Error submitting request:", error);
        }
    };

    const fetchRequests = async () => {
        try {
            const res = await axios.get("http://127.0.0.1:5000/holiday_requests", { headers });
            setRequests(res.data);
        } catch (error) {
            console.error("Error fetching requests:", error);
        }
    };

    const handleUpdate = async (id, newStatus) => {
        try {
            await axios.put(
                `http://127.0.0.1:5000/holiday_requests/${id}`,
                { status: newStatus },
                { headers }
            );
            fetchRequests();
        } catch (error) {
            console.error("Error updating request:", error);
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
            <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
            <button onClick={submitRequest}>Submit</button>

            <label>Filter by Status: </label>
            <select value={filter} onChange={(e) => setFilter(e.target.value)}>
                <option value="All">All</option>
                <option value="Pending">Pending</option>
                <option value="Approved">Approved</option>
                <option value="Rejected">Rejected</option>
            </select>

            <h3>Current Holiday Requests</h3>
            <table border="1">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Employee ID</th>
                        <th>Date</th>
                        <th>Status</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {requests
                        .filter((r) => filter === "All" || r.status === filter)
                        .map((r) => (
                            <tr key={r.id}>
                                <td>{r.id}</td>
                                <td>{r.employee_id}</td>
                                <td>{r.date}</td>
                                <td>{r.status}</td>
                                <td>
                                    <button onClick={() => handleUpdate(r.id, "Approved")}>Approve</button>
                                    <button onClick={() => handleUpdate(r.id, "Rejected")}>Reject</button>
                                </td>
                            </tr>
                        ))}
                </tbody>
            </table>
        </div>
    );
};

export default HolidayRequests;
