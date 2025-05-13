import React from 'react';
import { Card, Button, Row, Col } from 'antd';
import GraduateImg from '../assets/Graduate.jpg';
import './Services.css';
import { useNavigate } from 'react-router-dom';

const Services = () => {
  const navigate = useNavigate();
  return (
    <div className="services-container">
      <div className="services-header">
        <span className="services-prediction-label">STREAMLINDES PREDICTIONS</span>
        <h2 className="services-title">Effortlessly assess your graduation chances</h2>
      </div>
      <Row gutter={32} justify="center">
        <Col xs={24} md={12} lg={8}>
          <Card
            className="service-card"
            cover={<img alt="Graduation" src={GraduateImg} className="service-img" />}
            bordered={false}
          >
            <h3 className="service-card-title">Graduation Prediction</h3>
            <p className="service-card-desc">Forecast your graduation success</p>
            <Button block className="service-btn" onClick={() => navigate('/predict')}>View More</Button>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Services; 