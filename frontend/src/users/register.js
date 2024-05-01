import React, { useState } from 'react';
import UserService from '../services/userService';
import './login-register.css';
import { useNavigate, Link } from "react-router-dom";

function RegisterPage() {
    const [user, setUser] = useState({ email: '', password: '' });
    const [error, setError] = useState(null); // Initialize error as null for no error
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setUser({ ...user, [name]: value });
        setError(null);  // Reset error on any input change
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await UserService.register(user);
            console.log('Registration successful', response);
            navigate('/login'); // Redirect to login page after successful registration
        } catch (error) {
            console.error('Registration failed:', error);
            setError('Registration failed. Please try again.'); // Set a user-friendly error message
            setUser({ ...user, password: '' }); // Clear the password field to maintain security
        }
    };

    return (
        <div>
            <h2>Register</h2>
            <form onSubmit={handleSubmit}>
                <input type="email" name="email" placeholder="Email" value={user.email}
                       onChange={handleChange} required
                       className={error ? 'input-error' : ''}/>
                <input type="password" name="password" placeholder="Password" value={user.password}
                       onChange={handleChange} required
                       className={error ? 'input-error' : ''}/>
                {error && <div className="error">{error}</div>}
                <button type="submit">Register</button>
            </form>
            <div className={"link-box"}>
                <p>Back to login | </p>
                <Link to="/login">Login</Link>
            </div>
        </div>
    );
}

export default RegisterPage;
