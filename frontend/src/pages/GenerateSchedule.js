import React, { useState, useEffect } from "react";
import axios from "axios";

const GenerateSchedule = () => {
    const [startDate, setStartDate] = useState("");
    const [endDate, setEndDate] = useState("");
    const [schedule, setSchedule] = useState([]);

    const generateSchedule = async () => {
        try {
            await axios.post("http://127.0.0.1:5000/generate_schedule", {
                start_date: startDate,
                end_date: endDate,
            });
            fetchSchedule();
        } catch (error) {
            console.error("Error generating schedule:", error);
        }
    };

    const fetchSchedule = async () => {
        try {
            const res = await axios.get("http://127.0.0.1:5000/schedule");
            setSchedule(res.data);
        } catch (error) {
            console.error("Error fetching schedule:", error);
        }
    };

    useEffect(() => {
        fetchSchedule();
    }, []);

    return (
        <div>
            <h2>Generate Schedule</h2>
            <input type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} />
            <input type="date" value={endDate} onChange={(e) => setEndDate(e.target.value)} />
            <button onClick={generateSchedule}>Generate</button>

            <h3>Current Schedule</h3>
            <table border="1">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Shift Type</th>
                        <th>Start Time</th>
                        <th>End Time</th>
                        <th>Employee</th>
                        <th>Role</th>
                    </tr>
                </thead>
                <tbody>
                    {schedule.map((shift) => (
                        <tr key={shift.id}>
                            <td>{shift.date}</td>
                            <td>{shift.shift_type}</td>
                            <td>{shift.start_time}</td>
                            <td>{shift.end_time}</td>
                            <td>{shift.employee_id}</td>
                            <td>{shift.role}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

export default GenerateSchedule;
