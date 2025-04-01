import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import { UserContext } from "../App";

const GenerateSchedule = () => {
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [schedule, setSchedule] = useState([]);
  const [selectedDate, setSelectedDate] = useState("");
  const [employees, setEmployees] = useState([]);
  const { user } = useContext(UserContext);

  const fetchEmployees = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:5000/employees", {
        headers: { Authorization: `Bearer ${user.token}` },
        params: { user_id: user.id },
      });
      setEmployees(res.data);
    } catch (err) {
      console.error("Error fetching employees:", err);
    }
  };

  const fetchSchedule = async () => {
    try {
      if (!selectedDate) return;
      const res = await axios.get(`http://127.0.0.1:5000/schedule/${selectedDate}`, {
        headers: { Authorization: `Bearer ${user.token}` },
        params: { user_id: user.id },
      });
      setSchedule(res.data);
    } catch (err) {
      console.error("Error fetching schedule:", err);
    }
  };

  const generateSchedule = async () => {
    try {
      await axios.post(
        "http://127.0.0.1:5000/generate_schedule",
        {
          start_date: startDate,
          end_date: endDate,
          user_id: user.id,
        },
        {
          headers: { Authorization: `Bearer ${user.token}` },
        }
      );
      fetchSchedule();
    } catch (err) {
      console.error("Error generating schedule:", err);
    }
  };

  const deleteSchedule = async () => {
    if (!selectedDate) return;
    try {
      await axios.delete(`http://127.0.0.1:5000/schedule/${selectedDate}`, {
        headers: { Authorization: `Bearer ${user.token}` },
        params: { user_id: user.id },
      });
      setSchedule([]);
    } catch (err) {
      console.error("Error deleting schedule:", err);
    }
  };

  useEffect(() => {
    if (user) fetchEmployees();
  }, [user]);

  useEffect(() => {
    if (user && selectedDate) fetchSchedule();
  }, [selectedDate]);

  const getEmployeeName = (id) => {
    const emp = employees.find((e) => e.id === id);
    return emp ? emp.name : "Unknown";
  };

  // Sort schedule by role then AM before PM
  const sortedSchedule = [...schedule].sort((a, b) => {
    if (a.role < b.role) return -1;
    if (a.role > b.role) return 1;
    if (a.shift_type === "AM" && b.shift_type === "PM") return -1;
    if (a.shift_type === "PM" && b.shift_type === "AM") return 1;
    return 0;
  });

  return (
    <div style={{ padding: "20px" }}>
      <h2>Generate Schedule</h2>
      <div style={{ marginBottom: "10px" }}>
        <label>Start Date:</label>{" "}
        <input
          type="date"
          value={startDate}
          onChange={(e) => setStartDate(e.target.value)}
        />{" "}
        <label>End Date:</label>{" "}
        <input
          type="date"
          value={endDate}
          onChange={(e) => setEndDate(e.target.value)}
        />{" "}
        <button onClick={generateSchedule}>Generate</button>
      </div>

      <h3>View Schedule for a Specific Date</h3>
      <input
        type="date"
        value={selectedDate}
        onChange={(e) => setSelectedDate(e.target.value)}
      />
      <div className="schedule-controls">
        <button onClick={fetchSchedule}>View Schedule</button>
        <button onClick={deleteSchedule}>Delete Schedule</button>
      </div>

      {sortedSchedule.length > 0 ? (
        <table border="1" cellPadding="6" style={{ marginTop: "20px", width: "100%" }}>
          <thead>
            <tr>
              <th>Date</th>
              <th>Shift</th>
              <th>Start</th>
              <th>End</th>
              <th>Employee</th>
              <th>Role</th>
            </tr>
          </thead>
          <tbody>
            {sortedSchedule.map((s) => (
              <tr key={s.id}>
                <td>{s.date}</td>
                <td>{s.shift_type}</td>
                <td>{s.start_time}</td>
                <td>{s.end_time}</td>
                <td>{getEmployeeName(s.employee_id)}</td>
                <td>{s.role}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p style={{ marginTop: "20px" }}>No schedule for selected date.</p>
      )}
    </div>
  );
};

export default GenerateSchedule;

