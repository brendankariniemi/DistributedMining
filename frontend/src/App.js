import React from 'react';
import {BrowserRouter as Router, Navigate, Route, Routes} from 'react-router-dom';
import LoginPage from './users/login';
import RegisterPage from './users/register';
import ProfilePage from './users/profile';
import RewardsPage from "./rewards/rewards";
import ResourcesPage from "./resources/resources";
import PoolsPage from "./pools/pools";
import HomePage from './home';
import Menu from "./menu";
import LogoutPage from "./users/logout";
import Utils from './services/utils';

const ProtectedRoute = ({ children }) => {
    const token = Utils.getStorageItem('userToken');
    if (!token) {
        return <Navigate to="/login" replace />;
    }
    return children;
};

function App() {
    return (
        <Router>
            <Menu />
            <Routes>
                <Route path="/" element={<ProtectedRoute><HomePage /></ProtectedRoute>} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/logout" element={<LogoutPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/profile" element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />
                <Route path="/rewards" element={<ProtectedRoute><RewardsPage /></ProtectedRoute>} />
                <Route path="/pools" element={<ProtectedRoute><PoolsPage /></ProtectedRoute>} />
                <Route path="/resources" element={<ProtectedRoute><ResourcesPage /></ProtectedRoute>} />
                <Route path="*" element={<Navigate replace to="/" />} />
            </Routes>
        </Router>
    );
}

export default App;
