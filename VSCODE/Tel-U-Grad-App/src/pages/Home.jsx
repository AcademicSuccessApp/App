import React from 'react';
import { Button } from 'antd';
import { useNavigate } from 'react-router-dom';
import bg from '../assets/bg.jpg';
import './Home.css';

const Home = () => {
  const navigate = useNavigate();
  return (
    <div className="home-hero" style={{ backgroundImage: `url(${bg})` }}>
      <div className="home-overlay">
        <h1 className="home-title">PREDICT YOUR<br />GRADUATION</h1>
        <p className="home-subtitle">Know your chances of success</p>
        <Button
          type="primary"
          size="large"
          className="home-btn"
          onClick={() => navigate('/services')}
        >
          View Services
        </Button>
      </div>
    </div>
  );
};

export default Home; 