import React, { useState, useEffect } from "react";
import axios from "axios";

const AddEmployee = () => {
    const [name, setName] = useState("");
    const [role, setRole] = useState("");
    const [availability, setAvailability] = useState("");
    const [preferredHours, setPreferredHours] = useState(40);
    const [employees, setEmployees] = useState([]);
    const [editingId, setEditingId] = useState(null);  // Track which employee is being edited

    useEffect(() => {
        fetchEmployees();
    }, []);

    const fetchEmployees = async () => {
        try {
            const res = await axios.get("http://127.0.0.1:5000/employees");
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
            setName("");
            setRole("");
            setAvailability("");
            setPreferredHours(40);
            fetchEmployees(); // Refresh list
        } catch (error) {
            console.error("Error adding employee:", error);
        }
    };

    const deleteEmployee = async (id) => {
        try {
            await axios.delete(`http://127.0.0.1:5000/employees/${id}`);
            fetchEmployees(); // Refresh list after delete
        } catch (error) {
            console.error("Error deleting employee:", error);
        }
    };    

    const updateEmployee = async (id) => {
        try {
            await axios.put(`http://127.0.0.1:5000/employees/${id}`, {
                name,
                role,
                availability
            });
            setEditingId(null);
            fetchEmployees(); // Refresh list after update
        } catch (error) {
            console.error("Error updating employee:", error);
        }
    };
    

    return (
        <div>
            <h2>{editingId ? "Edit Employee" : "Add Employee"}</h2>
            <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} />
            <input type="text" placeholder="Role" value={role} onChange={(e) => setRole(e.target.value)} />
            <input type="text" placeholder="Availability (Mon-Fri 10:00-23:00)" value={availability} onChange={(e) => setAvailability(e.target.value)} />
            <input type="number" placeholder="Preferred Hours" value={preferredHours} onChange={(e) => setPreferredHours(e.target.value)} />
            {editingId ? (
                <button onClick={() => updateEmployee(editingId)}>Update Employee</button>
            ) : (
                <button onClick={addEmployee}>Add Employee</button>
            )}

            <h3>Current Employees</h3>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Role</th>
                        <th>Availability</th>
                    </tr>
                </thead>
                <tbody>
                    {employees.map((emp) => (
                        <tr key={emp.id}>
                            <td>{emp.id}</td>
                            <td>{editingId === emp.id ? (
                                <input
                                    type="text"
                                    value={name}
                                    onChange={(e) => setName(e.target.value)}
                                />
                            ) : (
                                emp.name
                            )}</td>
                            <td>{editingId === emp.id ? (
                                <input
                                    type="text"
                                    value={role}
                                    onChange={(e) => setRole(e.target.value)}
                                />
                            ) : (
                                emp.role
                            )}</td>
                            <td>{editingId === emp.id ? (
                                <input
                                    type="text"
                                    value={availability}
                                    onChange={(e) => setAvailability(e.target.value)}
                                />
                            ) : (
                                emp.availability
                            )}</td>
                            <td>
                                {editingId === emp.id ? (
                                    <button onClick={() => updateEmployee(emp.id)}>Save</button>
                                ) : (
                                    <>
                                        <button onClick={() => {
                                            setEditingId(emp.id);
                                            setName(emp.name);
                                            setRole(emp.role);
                                            setAvailability(emp.availability);
                                        }}>Edit</button>
                                        <button onClick={() => deleteEmployee(emp.id)}>Delete</button>
                                    </>
                                )}
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>


        </div>
    );
};

export default AddEmployee;
