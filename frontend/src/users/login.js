import React, { useState } from 'react';
import UserService from '../services/userService';
import { useNavigate, Link } from 'react-router-dom';
import './login-register.css';

function LoginPage() {
    const [credentials, setCredentials] = useState({ email: '', password: '' });
    const [error, setError] = useState(null);  // Use null to distinguish no error state
    const navigate = useNavigate();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setCredentials({...credentials, [name]: value});
        setError(null);  // Reset error on any input change
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await UserService.login(credentials);
            console.log('Login successful:', response);
            navigate('/');  // Navigate to homepage or dashboard on successful login
        } catch (error) {
            console.error('Login failed:', error);
            setError('Failed to login. Check your email and password.'); // Set a user-friendly error message
            setCredentials(prev => ({ ...prev, password: '' }));  // Clear the password field only
        }
    };

    return (
        <div>
            <h2>Login</h2>
            <form onSubmit={handleSubmit}>
                <input type="text" name="email" placeholder="Email" value={credentials.email}
                       onChange={handleChange} required
                       className={error ? 'input-error' : ''}/>
                <input type="password" name="password" placeholder="Password" value={credentials.password}
                       onChange={handleChange} required
                       className={error ? 'input-error' : ''}/>
                {error && <div className="error">{error}</div>}
                <button type="submit">Login</button>
            </form>
            <div className={"link-box"}>
                <p>Don't have an account? | </p>
                <Link to="/register">Register</Link>
            </div>
        </div>
    );
}

export default LoginPage;
