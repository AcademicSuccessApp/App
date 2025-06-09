import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Card, Button, Typography, Row, Col, Progress } from 'antd';
import { CheckCircleOutlined, WarningOutlined, ClockCircleOutlined } from '@ant-design/icons';
import './Result.css';

const { Title, Text } = Typography;

const Result = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { classification, regression, recommendation, ...formData } = location.state || {};

  if (!location.state) {
    return (
      <div className="result-container">
        <Card className="result-card">
          <Title level={3}>No Prediction Data</Title>
          <Text>Please go back and make a prediction first.</Text>
          <Button type="primary" onClick={() => navigate('/predict')} style={{ marginTop: 20 }}>
            Make Prediction
          </Button>
        </Card>
      </div>
    );
  }

  const isLikelyToGraduate = classification.status === 'Likely to Graduate on Time';

  return (
    <div className="result-container">
      <Card className="result-card">
        <Title level={2} className="result-title">Prediction Result</Title>
        
        {/* Classification Result */}
        <div className="result-status" style={{ justifyContent: 'center', marginBottom: 32, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Progress
            type="circle"
            percent={Math.round(classification.probability * 100)}
            strokeColor={isLikelyToGraduate ? '#52c41a' : '#f5222d'}
            format={percent => `${percent}%`}
            width={120}
            style={{ marginBottom: 16 }}
          />
          {isLikelyToGraduate ? (
            <CheckCircleOutlined style={{ fontSize: 48, color: '#52c41a', marginTop: 16 }} />
          ) : (
            <WarningOutlined style={{ fontSize: 48, color: '#f5222d', marginTop: 16 }} />
          )}
          <Title level={3}>{classification.status}</Title>
          <Text style={{ fontSize: 24, color: isLikelyToGraduate ? '#52c41a' : '#f5222d' }}>
            {Math.round(classification.probability * 100)}% Confidence
          </Text>
        </div>

        {/* Regression Result */}
        <div className="regression-result" style={{ textAlign: 'center', marginBottom: 32 }}>
          <ClockCircleOutlined style={{ fontSize: 48, color: '#1890ff', marginBottom: 16 }} />
          <Title level={3}>Predicted Graduation Time</Title>
          <Text style={{ fontSize: 36, color: '#1890ff', fontWeight: 'bold' }}>
            Semester {Math.round(regression.predicted_semester)}
          </Text>
          <Text type="secondary" style={{ display: 'block', marginTop: 8 }}>
            {isLikelyToGraduate ? 'Expected to graduate on time' : 'May take longer than expected'}
          </Text>
        </div>

        {/* Input Details */}
        <div className="result-details">
          <Title level={4}>Input Details</Title>
          <Row gutter={[16, 16]}>
            <Col span={12}>
              <Text strong>Semester 1 IPS:</Text>
              <Text>{formData.sem1}</Text>
            </Col>
            <Col span={12}>
              <Text strong>Semester 2 IPS:</Text>
              <Text>{formData.sem2}</Text>
            </Col>
            <Col span={12}>
              <Text strong>Semester 3 IPS:</Text>
              <Text>{formData.sem3}</Text>
            </Col>
            <Col span={12}>
              <Text strong>Semester 4 IPS:</Text>
              <Text>{formData.sem4}</Text>
            </Col>
            <Col span={12}>
              <Text strong>Gender:</Text>
              <Text>{formData.gender}</Text>
            </Col>
            <Col span={12}>
              <Text strong>Program Studi:</Text>
              <Text>{formData.programStudi}</Text>
            </Col>
          </Row>
        </div>

        {/* Recommendation */}
        <div className="result-recommendation">
          <Title level={4}>Recommendation</Title>
          <Text>{recommendation}</Text>
        </div>

        {/* Actions */}
        <div className="result-actions">
          <Button type="primary" onClick={() => navigate('/predict')}>
            Make Another Prediction
          </Button>
        </div>
      </Card>
    </div>
  );
};

export default Result; 