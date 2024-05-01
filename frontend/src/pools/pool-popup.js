import React, { useState } from 'react';
import PoolService from '../services/poolService';
import './pool-popup.css';

function PoolPopUp({ toggle, pool_id }) {
    const [hardwareInfo, setHardwareInfo] = useState({
        ip_address: '',
        hash_rate: '',
        python_path: '',
        client_path: '',
	pool: pool_id
    });
    const [error, setError] = useState(null);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setHardwareInfo({ ...hardwareInfo, [name]: value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
	    console.log(hardwareInfo)
            const response = await PoolService.registerHardware(hardwareInfo);
            console.log('Registration successful', response);
            toggle(); // Toggle only on successful registration
        } catch (error) {
            console.error('Registration failed:', error);
            setError('Registration failed. Please try again.');
            setHardwareInfo({ ...hardwareInfo, ip_address: '', hash_rate: '', python_path: '', client_path: '' });
        }
    };

    return (
        <div className="modal-backdrop">
            <div className="modal-content">
                <h2>Register</h2>
                <form onSubmit={handleSubmit}> {/* Use handleSubmit here */}
                    <label>
                        IP Address:
                        <input type="text" name="ip_address" value={hardwareInfo.ip_address} onChange={handleChange} className={error ? 'input-error' : ''}/>
                    </label>
                    <label>
                        Hash Rate:
                        <input type="text" name="hash_rate" value={hardwareInfo.hash_rate} onChange={handleChange} className={error ? 'input-error' : ''}/>
                    </label>
                    <label>
                        Python Path:
                        <input type="text" name="python_path" value={hardwareInfo.python_path} onChange={handleChange} className={error ? 'input-error' : ''}/>
                    </label>
                    <label>
                        Client Path:
                        <input type="text" name="client_path" value={hardwareInfo.client_path} onChange={handleChange} className={error ? 'input-error' : ''}/>
                    </label>
                    <div className="button-group">
                        <button type="submit">Register</button>
                        <button type="button" onClick={toggle}>Close</button>
                    </div>
                </form>
            </div>
        </div>
    );
}

export default PoolPopUp;

