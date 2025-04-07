import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import { UserContext } from "../App";

const Account = () => {
  const { user } = useContext(UserContext);
  const [form, setForm] = useState({ username: "", email: "", password: "" });

  useEffect(() => {
    const fetchAccount = async () => {
      const res = await axios.get("http://127.0.0.1:5000/account", {
        headers: { Authorization: `Bearer ${user.token}` },
      });
      setForm({ ...form, username: res.data.username, email: res.data.email });
    };
    if (user?.token) fetchAccount();
  }, [user]);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    await axios.put("http://127.0.0.1:5000/account", form, {
      headers: { Authorization: `Bearer ${user.token}` },
    });
    alert("Account updated");
    setForm({ ...form, password: "" });
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>My Account</h2>
      <form onSubmit={handleSubmit}>
        <input name="username" value={form.username} onChange={handleChange} placeholder="Username" required />
        <input name="email" type="email" value={form.email} onChange={handleChange} placeholder="Email" required />
        <input name="password" type="password" value={form.password} onChange={handleChange} placeholder="New Password" />
        <button type="submit">Update Account</button>
      </form>
    </div>
  );
};

export default Account;
