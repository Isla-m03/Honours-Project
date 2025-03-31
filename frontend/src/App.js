import React from "react";
import { BrowserRouter as Router, Route, Routes, Navigate } from "react-router-dom";
import AddEmployee from "./AddEmployee";
import Forecast from "./Forecast";
import GenerateSchedule from "./GenerateSchedule";
import HolidayRequests from "./HolidayRequests";

const App = () => {
    const token = localStorage.getItem("token");

    return (
        <Router>
            <Routes>
                <Route path="/" element={token ? <Navigate to="/employees" /> : <Navigate to="/login" />} />
                <Route path="/employees" element={<AddEmployee />} />
                <Route path="/forecast" element={<Forecast />} />
                <Route path="/schedule" element={<GenerateSchedule />} />
                <Route path="/holidays" element={<HolidayRequests />} />
            </Routes>
        </Router>
    );
};

export default App;

