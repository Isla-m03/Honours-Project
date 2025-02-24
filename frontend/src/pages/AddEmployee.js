import React, { useState, useEffect } from "react";
import axios from "axios";

const AddEmployee = () => {
    const [name, setName] = useState("");
    const [role, setRole] = useState("");
    const [availability, setAvailability] = useState("");
    const [preferredHours, setPreferredHours] = useState(40);
    const [employees, setEmployees] = useState([]);

    useEffect(() => {
        fetchEmployees();
    }, []);

    const fetchEmployees = async () => {
        try {
            const res = await axios.get("http://127.0.0.1:5000/employees");
            console.log("Fetched Employees:", res.data);  // Debugging
            setEmployees(res.data);
        } catch (error) {
            console.error("Error fetching employees:", error);
        }
    };
    

    const addEmployee = async () => {
        try {
            await axios.post("http://127.0.0.1:5000/employees", {
                name,
                role,
                availability,
                preferred_hours: preferredHours,
            });
            fetchEmployees(); // Refresh list
        } catch (error) {
            console.error("Error adding employee:", error);
        }
    };

    return (
        <div>
            <h2>Add Employee</h2>
            <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
            <input type="text" placeholder="Role" value={role} onChange={(e) => setRole(e.target.value)} />
            <input type="text" placeholder="Availability (Mon-Fri 10:00-23:00)" value={availability} onChange={(e) => setAvailability(e.target.value)} />
            <input type="number" placeholder="Preferred Hours" value={preferredHours} onChange={(e) => setPreferredHours(e.target.value)} />
            <button onClick={addEmployee}>Add Employee</button>

            <h3>Current Employees</h3>
            <ul>
                {employees.map((emp) => (
                    <li key={emp.id}>{emp.name} - {emp.role} ({emp.availability})</li>
                ))}
            </ul>
        </div>
    );
};

export default AddEmployee;

