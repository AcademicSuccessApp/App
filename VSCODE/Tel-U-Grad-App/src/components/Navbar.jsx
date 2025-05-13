import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Button, Menu } from 'antd';
import './Navbar.css';
import logo from '../assets/logo.png';

const menuItems = [
  { label: <Link to="/">Home</Link>, key: '/' },
  { label: <Link to="/about">About</Link>, key: '/about' },
  { label: <Link to="/services">Services</Link>, key: '/services' },
  { label: <Link to="/how-it-works">How It Works</Link>, key: '/how-it-works' },
];

const Navbar = () => {
  const location = useLocation();
  return (
    <nav className="navbar-container">
      <div className="navbar-logo">
        <img src={logo} alt="Tel-U GRAD Logo" height={60} />
      </div>
      <Menu
        mode="horizontal"
        selectedKeys={[location.pathname]}
        items={menuItems}
        className="navbar-menu"
      />
      <div className="navbar-contact">
        <Link to="/contact">
          <Button type="default" className="contact-btn">CONTACT</Button>
        </Link>
      </div>
    </nav>
  );
};

export default Navbar; 