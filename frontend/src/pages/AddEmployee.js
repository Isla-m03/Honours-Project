import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import { UserContext } from "../App";

const AddEmployee = () => {
  const { user } = useContext(UserContext);
  const token = user?.token;

  const [employees, setEmployees] = useState([]);
  const [filteredEmployees, setFilteredEmployees] = useState([]);
  const [selectedRole, setSelectedRole] = useState("All");

  const [form, setForm] = useState({
    name: "",
    role: "",
    availability: "",
    preferred_hours: 40,
  });
  const [editId, setEditId] = useState(null);

  const fetchEmployees = async () => {
    try {
      const res = await axios.get("http://localhost:5000/employees", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setEmployees(res.data);
      setFilteredEmployees(res.data);
    } catch (err) {
      console.error("Error fetching employees:", err);
    }
  };

  const handleRoleFilter = (e) => {
    const role = e.target.value;
    setSelectedRole(role);
    if (role === "All") {
      setFilteredEmployees(employees);
    } else {
      setFilteredEmployees(employees.filter((emp) => emp.role === role));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (editId) {
        await axios.put(
          `http://localhost:5000/employees/${editId}`,
          form,
          {
            headers: { Authorization: `Bearer ${token}` },
          }
        );
        setEditId(null);
      } else {
        await axios.post("http://localhost:5000/employees", form, {
          headers: { Authorization: `Bearer ${token}` },
        });
      }
      setForm({ name: "", role: "", availability: "", preferred_hours: 40 });
      fetchEmployees();
    } catch (err) {
      console.error("Error submitting employee:", err);
    }
  };

  const handleDelete = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/employees/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchEmployees();
    } catch (err) {
      console.error("Error deleting employee:", err);
    }
  };

  const handleEdit = (emp) => {
    setEditId(emp.id);
    setForm({
      name: emp.name,
      role: emp.role,
      availability: emp.availability,
      preferred_hours: emp.preferred_hours,
    });
  };

  useEffect(() => {
    if (token) fetchEmployees();
  }, [token]);

  useEffect(() => {
    handleRoleFilter({ target: { value: selectedRole } });
  }, [employees]);

  return (
    <div style={{ padding: 20 }}>
      <h2>{editId ? "Edit Employee" : "Add Employee"}</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Name"
          value={form.name}
          onChange={(e) => setForm({ ...form, name: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Role"
          value={form.role}
          onChange={(e) => setForm({ ...form, role: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Availability"
          value={form.availability}
          onChange={(e) => setForm({ ...form, availability: e.target.value })}
        />
        <input
          type="number"
          placeholder="Preferred Hours"
          value={form.preferred_hours}
          onChange={(e) =>
            setForm({ ...form, preferred_hours: e.target.value })
          }
        />
        <button type="submit">{editId ? "Update" : "Add"} Employee</button>
      </form>
      
      <br></br>
      <h3>Current Employees</h3>

      <label>Filter by Role: </label>
      <select value={selectedRole} onChange={handleRoleFilter}>
        <option value="All">All</option>
        {[...new Set(employees.map((emp) => emp.role))].map((role) => (
          <option key={role} value={role}>
            {role}
          </option>
        ))}
      </select>

      <table border="1" cellPadding="8" style={{ width: "100%", marginTop: "10px" }}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Role</th>
            <th>Availability</th>
            <th>Preferred Hours</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {filteredEmployees.map((emp) => (
            <tr key={emp.id}>
              <td>{emp.id}</td>
              <td>{emp.name}</td>
              <td>{emp.role}</td>
              <td>{emp.availability}</td>
              <td>{emp.preferred_hours}</td>
              <td>
                <button onClick={() => handleEdit(emp)}>Edit</button>
                <button onClick={() => handleDelete(emp.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AddEmployee;
