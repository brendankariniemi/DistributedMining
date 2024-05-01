import React, { useState, useEffect } from 'react';
import UserService from '../services/userService';
import './profile.css';

function ProfilePage() {
    const [profile, setProfile] = useState({ email: '', password: '' });
    const [isEditing, setIsEditing] = useState(false);
    const [error, setError] = useState(''); // Added to manage error messages

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                const response = await UserService.getProfile();
                setProfile({ email: response.data.email, password: '' }); // Don't fetch password
            } catch (error) {
                console.error('Failed to fetch profile:', error);
                setError('Unable to load profile. Please try again later.');
            }
        };

        fetchProfile();
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setProfile({ ...profile, [name]: value });
        setError(''); // Reset error messages when user starts editing
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!profile.email) {
            setError('Email is required.');
            return;
        }
        try {
            await UserService.updateProfile({ email: profile.email, password: profile.password.trim() ? profile.password : undefined });
            console.log('Profile updated successfully');
            setIsEditing(false);
            setError('');
        } catch (error) {
            console.error('Failed to update profile:', error);
            setError('Failed to update profile. Please check your data and try again.');
        }
    };

    return (
        <div>
            <h2>Profile</h2>
            {!isEditing ? (
                <div>
                    <p>Email: {profile.email}</p>
                    <button onClick={() => setIsEditing(true)}>Edit</button>
                </div>
            ) : (
                <form onSubmit={handleSubmit}>
                    <div>
                        <label>Email:</label>
                        <input type="email" name="email" value={profile.email} onChange={handleChange} required />
                    </div>
                    <div>
                        <label>Password (leave blank to keep unchanged):</label>
                        <input type="password" name="password" value={profile.password} onChange={handleChange} />
                    </div>
                    {error && <div className="error-message">{error}</div>}
                    <button type="submit">Save Changes</button>
                    <button type="button" onClick={() => setIsEditing(false)}>Cancel</button>
                </form>
            )}
        </div>
    );
}

export default ProfilePage;
