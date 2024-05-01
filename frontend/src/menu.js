import { NavLink } from 'react-router-dom'
import './menu.css'

const Menu = () => {
    return (
        <nav className="menu-container">
            <div className="menu-header">CSCI 414 - Distributed Mining</div>
            <div className="menu-links">
                <NavLink to="/" className="menu-link">Home</NavLink>
                <NavLink to="/rewards" className="menu-link">Rewards</NavLink>
                <NavLink to="/pools" className="menu-link">Pools</NavLink>
                <NavLink to="/resources" className="menu-link">Resources</NavLink>
                <NavLink to="/profile" className="menu-link">Profile</NavLink>
                <NavLink to="/logout" className="menu-link">Logout</NavLink>
            </div>
        </nav>
    );
}

export default Menu;