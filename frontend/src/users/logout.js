import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import UserService from '../services/userService';

const LogoutPage = () => {
    const navigate = useNavigate();

    useEffect(() => {
        // Perform the logout operation
        UserService.logout();
        navigate('/login', { replace: true });
    }, [navigate]);

    return (
        <div>Logging out...</div>
    );
}

export default LogoutPage;
