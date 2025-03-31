import React, { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { UserContext } from "./App";

const Navbar = () => {
  const { user, logout } = useContext(UserContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav style={styles.navbar}>
      <h2 style={styles.logo}>ShiftSync</h2>
      <div style={styles.links}>
        {user ? (
          <>
            <Link to="/employees" style={styles.link}>Employees</Link>
            <Link to="/forecast" style={styles.link}>Forecast</Link>
            <Link to="/schedule" style={styles.link}>Schedule</Link>
            <Link to="/holiday" style={styles.link}>Holiday</Link>
            <button onClick={handleLogout} style={styles.button}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" style={styles.link}>Login</Link>
            <Link to="/register" style={styles.link}>Register</Link>
          </>
        )}
      </div>
    </nav>
  );
};

const styles = {
  navbar: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "10px 20px",
    backgroundColor: "#1e1e2f",
    color: "white"
  },
  logo: {
    margin: 0
  },
  links: {
    display: "flex",
    gap: "15px"
  },
  link: {
    color: "white",
    textDecoration: "none"
  },
  button: {
    backgroundColor: "#6a0dad",
    color: "white",
    border: "none",
    padding: "6px 12px",
    cursor: "pointer"
  }
};

export default Navbar;
