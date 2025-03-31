import React, { useState, useEffect } from "react";
import axios from "axios";

const GenerateSchedule = () => {
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [schedule, setSchedule] = useState([]);
    const [employees, setEmployees] = useState([]);
    const [selectedDate, setSelectedDate] = useState("");

    const token = localStorage.getItem("token");
    const headers = { Authorization: `Bearer ${token}` };

    const fetchEmployees = async () => {
        try {
            const res = await axios.get("http://127.0.0.1:5000/employees", { headers });
            setEmployees(res.data);
        } catch (error) {
            console.error("Error fetching employees:", error);
        }
    };

    const fetchSchedule = async (date = null) => {
        try {
            const url = date ? `http://127.0.0.1:5000/schedule/${date}` : "http://127.0.0.1:5000/schedule";
            const res = await axios.get(url, { headers });
            setSchedule(res.data);
        } catch (error) {
            console.error("Error fetching schedule:", error);
        }
    };

    const generateSchedule = async () => {
        try {
            await axios.post(
                "http://127.0.0.1:5000/generate_schedule",
                { start_date: startDate, end_date: endDate },
                { headers }
            );
            fetchSchedule();
        } catch (error) {
            console.error("Error generating schedule:", error);
        }
    };

    const deleteSchedule = async () => {
        if (!selectedDate) {
            alert("Please select a date first.");
            return;
        }
        try {
            await axios.delete(`http://127.0.0.1:5000/schedule/${selectedDate}`, { headers });
            fetchSchedule();
        } catch (error) {
            console.error("Error deleting schedule:", error);
        }
    };

    useEffect(() => {
        fetchEmployees();
        fetchSchedule();
    }, []);

    useEffect(() => {
        if (selectedDate) fetchSchedule(selectedDate);
    }, [selectedDate]);

    const getEmployeeName = (id) => {
        if (!id) return "Unassigned";
        const employee = employees.find(emp => emp.id === id);
        return employee ? employee.name : `Employee ID: ${id}`;
    };

    const groupedShifts = schedule.reduce((acc, shift) => {
        if (!acc[shift.role]) acc[shift.role] = [];
        acc[shift.role].push(shift);
        return acc;
    }, {});

    return (
        <div className="container">
            <h2>Generate & Manage Schedule</h2>

            <div className="form">
                <label>Start Date:</label>
                <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
                <label>End Date:</label>
                <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
                <button onClick={generateSchedule} className="generate-btn">Generate Schedule</button>
            </div>

            <div className="filter">
                <label>View Schedule for Date:</label>
                <input type="date" value={selectedDate} onChange={(e) => setSelectedDate(e.target.value)} />
                <button onClick={deleteSchedule} className="delete-btn">Delete Schedule</button>
            </div>

            {selectedDate && schedule.length > 0 ? (
                Object.keys(groupedShifts).map((role) => (
                    <div key={role} className="schedule-section">
                        <h3>{role}</h3>
                        <table className="schedule-table">
                            <thead>
                                <tr>
                                    <th>Employee</th>
                                    <th>Shift Type</th>
                                    <th>Start Time</th>
                                    <th>End Time</th>
                                </tr>
                            </thead>
                            <tbody>
                                {groupedShifts[role].map((shift) => (
                                    <tr key={shift.id}>
                                        <td>{getEmployeeName(shift.employee_id)}</td>
                                        <td>{shift.shift_type}</td>
                                        <td>{shift.start_time}</td>
                                        <td>{shift.end_time}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                ))
            ) : (
                <p>No shifts scheduled for this date.</p>
            )}
        </div>
    );
};

export default GenerateSchedule;
