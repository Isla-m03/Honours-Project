
import React, { useState, useEffect } from "react";
import axios from "axios";

const AddEmployee = () => {
    const [employees, setEmployees] = useState([]);
    const [formData, setFormData] = useState({
        name: "",
        role: "",
        availability: "",
        preferred_hours: 40,
    });

    const token = localStorage.getItem("token");

    const fetchEmployees = async () => {
        try {
            const res = await axios.get("http://127.0.0.1:5000/employees", {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setEmployees(res.data);
        } catch (error) {
            console.error("Error fetching employees:", error);
        }
    };

    const handleAdd = async () => {
        try {
            await axios.post("http://127.0.0.1:5000/employees", formData, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            fetchEmployees();
        } catch (error) {
            console.error("Error adding employee:", error);
        }
    };

    useEffect(() => {
        fetchEmployees();
    }, []);

    return (
        <div>
            <h2>Add Employee</h2>
            <input placeholder="Name" value={formData.name} onChange={(e) => setFormData({...formData, name: e.target.value})} />
            <input placeholder="Role" value={formData.role} onChange={(e) => setFormData({...formData, role: e.target.value})} />
            <input placeholder="Availability" value={formData.availability} onChange={(e) => setFormData({...formData, availability: e.target.value})} />
            <input placeholder="Preferred Hours" type="number" value={formData.preferred_hours} onChange={(e) => setFormData({...formData, preferred_hours: parseInt(e.target.value)})} />
            <button onClick={handleAdd}>Add</button>

            <h3>Current Employees</h3>
            <ul>
                {employees.map((emp) => (
                    <li key={emp.id}>{emp.name} - {emp.role}</li>
                ))}
            </ul>
        </div>
    );
};

export default AddEmployee;
