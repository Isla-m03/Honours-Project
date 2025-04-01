import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import { UserContext } from "../App";

const HolidayRequests = () => {
  const [requests, setRequests] = useState([]);
  const [form, setForm] = useState({ employee_id: "", date: "" });
  const { user } = useContext(UserContext);

  const fetchRequests = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:5000/holiday_requests", {
        headers: { Authorization: `Bearer ${user.token}` },
        params: { user_id: user.id }
      });
      setRequests(res.data);
    } catch (err) {
      console.error("❌ Error fetching requests:", err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post(
        "http://127.0.0.1:5000/holiday_requests",
        {
          employee_id: form.employee_id,
          date: form.date,
          user_id: user.id
        },
        { headers: { Authorization: `Bearer ${user.token}` } }
      );
      setForm({ employee_id: "", date: "" });
      fetchRequests();
    } catch (err) {
      console.error("❌ Error submitting request:", err);
    }
  };

  const handleUpdate = async (requestId, newStatus) => {
    try {
      await axios.put(
        `http://127.0.0.1:5000/holiday_requests/${requestId}`,
        { status: newStatus },
        { headers: { Authorization: `Bearer ${user.token}` } }
      );
      fetchRequests();
    } catch (err) {
      console.error("❌ Error updating request:", err);
    }
  };

  useEffect(() => {
    if (user) fetchRequests();
  }, [user]);

  return (
    <div style={{ padding: "20px" }}>
      <h2>Holiday Request</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <input
          type="number"
          placeholder="Employee ID"
          value={form.employee_id}
          onChange={(e) => setForm({ ...form, employee_id: e.target.value })}
          required
        />
        <input
          type="date"
          value={form.date}
          onChange={(e) => setForm({ ...form, date: e.target.value })}
          required
        />
        <button type="submit">Submit Request</button>
      </form>

      <h3>Current Requests</h3>
      <table border="1" cellPadding="8" style={{ width: "100%" }}>
        <thead>
          <tr>
            <th>Employee ID</th>
            <th>Employee Name</th>
            <th>Date</th>
            <th>Status</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {requests.map((req) => (
            <tr key={req.id}>
              <td>{req.employee_id}</td>
              <td>{req.employee_name || "Unknown"}</td>
              <td>{req.date}</td>
              <td>{req.status}</td>
              <td>
                <button onClick={() => handleUpdate(req.id, "Approved")}>Approve</button>{" "}
                <button onClick={() => handleUpdate(req.id, "Rejected")}>Reject</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default HolidayRequests;
