import React, { useState } from "react";
import axios from "axios";

const AddEmployee = () => {
    const [name, setName] = useState("");
    const [role, setRole] = useState("");
    const [availability, setAvailability] = useState("");
    const [preferredHours, setPreferredHours] = useState(40);
    const [response, setResponse] = useState("");

    const addEmployee = async () => {
        try {
            const res = await axios.post("http://127.0.0.1:5000/employees", {
                name,
                role,
                availability,
                preferred_hours: preferredHours,
            });
            setResponse(res.data.message);
        } catch (error) {
            setResponse("Error adding employee");
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
            <p>{response}</p>
        </div>
    );
};

export default AddEmployee;
