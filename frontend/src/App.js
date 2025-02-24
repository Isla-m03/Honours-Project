import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import GenerateSchedule from "./pages/GenerateSchedule";
import AddEmployee from "./pages/AddEmployee";
import Forecast from "./pages/Forecast";
import HolidayRequests from "./pages/HolidayRequests";

const App = () => {
    return (
        <Router>
            <div style={{ padding: "20px" }}>
                <h1>Workplace Scheduler</h1>
                <nav style={{ marginBottom: "20px" }}>
                    <Link to="/" style={{ marginRight: "10px" }}>Generate Schedule</Link> | 
                    <Link to="/add-employee" style={{ marginRight: "10px" }}>Add Employee</Link> | 
                    <Link to="/forecast" style={{ marginRight: "10px" }}>Update Forecast</Link> | 
                    <Link to="/holiday-requests">Holiday Requests</Link>
                </nav>
                <Routes>
                    <Route path="/" element={<GenerateSchedule />} />
                    <Route path="/add-employee" element={<AddEmployee />} />
                    <Route path="/forecast" element={<Forecast />} />
                    <Route path="/holiday-requests" element={<HolidayRequests />} />
                </Routes>
            </div>
        </Router>
    );
};

export default App;

