import React, { useState, useEffect } from "react";
import axios from "axios";

const AddEmployee = () => {
  const [name, setName] = useState("");
  const [role, setRole] = useState("");
  const [availability, setAvailability] = useState("");
  const [preferredHours, setPreferredHours] = useState(40);
  const [employees, setEmployees] = useState([]);

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

  const addEmployee = async () => {
    try {
      await axios.post(
        "http://127.0.0.1:5000/employees",
        { name, role, availability, preferred_hours: preferredHours },
        { headers }
      );
      setName("");
      setRole("");
      setAvailability("");
      setPreferredHours(40);
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
      <input value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" />
      <input value={role} onChange={(e) => setRole(e.target.value)} placeholder="Role" />
      <input value={availability} onChange={(e) => setAvailability(e.target.value)} placeholder="Availability" />
      <input
        type="number"
        value={preferredHours}
        onChange={(e) => setPreferredHours(e.target.value)}
        placeholder="Preferred Hours"
      />
      <button onClick={addEmployee}>Add</button>

      <h3>Current Employees</h3>
      <table border="1">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Role</th>
            <th>Availability</th>
          </tr>
        </thead>
        <tbody>
          {employees.map((e) => (
            <tr key={e.id}>
              <td>{e.id}</td>
              <td>{e.name}</td>
              <td>{e.role}</td>
              <td>{e.availability}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AddEmployee;
