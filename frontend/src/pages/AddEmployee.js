import React, { useEffect, useState, useContext } from "react";
import axios from "axios";
import { UserContext } from "../App";

const AddEmployee = () => {
  const { user } = useContext(UserContext);
  const token = user?.token;

  const [employees, setEmployees] = useState([]);
  const [form, setForm] = useState({ name: "", role: "", availability: "", preferred_hours: 40 });

  const fetchEmployees = async () => {
    try {
      const res = await axios.get("http://localhost:5000/employees", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setEmployees(res.data);
    } catch (err) {
      console.error("Fetch Employees Error:", err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://localhost:5000/employees", form, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setForm({ name: "", role: "", availability: "", preferred_hours: 40 });
      fetchEmployees();
    } catch (err) {
      console.error("Add Employee Error:", err);
    }
  };

  useEffect(() => {
    if (token) fetchEmployees();
  }, [token]);

  return (
    <div style={{ padding: 20 }}>
      <h2>Add Employee</h2>
      <form onSubmit={handleSubmit}>
        <input placeholder="Name" value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} required />
        <input placeholder="Role" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })} required />
        <input placeholder="Availability" value={form.availability} onChange={(e) => setForm({ ...form, availability: e.target.value })} required />
        <input type="number" placeholder="Preferred Hours" value={form.preferred_hours} onChange={(e) => setForm({ ...form, preferred_hours: e.target.value })} />
        <button type="submit">Add</button>
      </form>

      <h3>Current Employees</h3>
      <ul>
        {employees.map(emp => (
          <li key={emp.id}>{emp.name} ({emp.role}) - {emp.availability}</li>
        ))}
      </ul>
    </div>
  );
};

export default AddEmployee;
