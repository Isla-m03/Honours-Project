import React, { useState, useEffect, createContext } from "react";
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./Navbar";
import AddEmployee from "./pages/AddEmployee";
import Forecast from "./pages/Forecast";
import GenerateSchedule from "./pages/GenerateSchedule";
import HolidayRequests from "./pages/HolidayRequests";
import Login from "./pages/Login";
import Register from "./pages/Register";

export const UserContext = createContext();

const App = () => {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem("token");
    return stored ? { token: stored } : null;
  });

  useEffect(() => {
    localStorage.removeItem("token");
    setUser(null);
  }, []);

  const login = (token) => {
    localStorage.setItem("token", token);
    setUser({ token });
  };

  const logout = () => {
    localStorage.removeItem("token");
    setUser(null);
  };

  return (
    <UserContext.Provider value={{ user, login, logout }}>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/employees" element={user ? <AddEmployee /> : <Navigate to="/login" />} />
          <Route path="/forecast" element={user ? <Forecast /> : <Navigate to="/login" />} />
          <Route path="/schedule" element={user ? <GenerateSchedule /> : <Navigate to="/login" />} />
          <Route path="/holiday" element={user ? <HolidayRequests /> : <Navigate to="/login" />} />
        </Routes>
      </Router>
    </UserContext.Provider>
  );
};

export default App;
