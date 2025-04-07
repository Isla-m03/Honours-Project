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
      <div style={styles.left}>
        <img src="/logo.png" alt="Logo" style={styles.logo} />
      </div>
      <div style={styles.links}>
        {user ? (
          <>
            <Link to="/employees" style={styles.link}>Employees</Link>
            <Link to="/forecast" style={styles.link}>Forecast</Link>
            <Link to="/schedule" style={styles.link}>Schedule</Link>
            <Link to="/holiday" style={styles.link}>Holiday</Link>
            <Link to="/account" style={styles.link}>Account</Link>
            <button className="logout-btn" onClick={handleLogout}>Logout</button>
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
  left: {
    display: "flex",
    alignItems: "center",
    gap: "10px"
  },
  logo: {
    height: "170px"
  },
  title: {
    margin: 0
  },
  links: {
    display: "flex",
    gap: "15px"
  },
  link: {
    color: "white",
    textDecoration: "none"
  }
};

export default Navbar;
