import React, { useState } from 'react';
import { Form, InputNumber, Select, Button, Row, Col, message, Spin } from 'antd';
import { useNavigate } from 'react-router-dom';
import { predictGraduation } from '../api/prediction';
import graduateCharacter from '../assets/Graduate Character.png';
import bg from '../assets/bg.jpg';
import './Prediction.css';

const { Option } = Select;

const programStudiOptions = [
  'S1 Teknik Informatika - Kampus Purwokerto',
  'S1 Sistem Informasi - Kampus Purwokerto',
  'S1 Rekayasa Perangkat Lunak - Kampus Purwokerto',
  'S1 Sains Data - Kampus Purwokerto'
];

const kodeDosenOptions = [
  'ANT', 'YRF', 'IQK', 'MLU', 'CPR', 'DAP', 'DSA', 'SDN', 'WAA', 'PRX', 'MAL', 'DCF',
  'NAP', 'AIZ', 'UMT', 'THX', 'ADN', 'ABD', 'ADO', 'YAK', 'ABX', 'MPT', 'TWR', 'SDX',
  'AGI', 'MFI', 'NAY', 'APT', 'WAX', 'TGL', 'FMW', 'ARI', 'IPA', 'EII', 'AWD', 'IST',
  'AJU', 'MZN', 'DSP', 'RDR', 'STX', 'RDN', 'EUA', 'FDD', 'DWA', 'RSY', 'SFR', 'MYK',
  'HWU', 'SWX', 'CRA', 'KMN', 'YDO', 'SAT', 'DJA', 'YUH', 'DYX', 'CWA', 'AAH', 'ARB',
  'GFA', 'AJS', 'NGN', 'NAR', 'ACW', 'AWT', 'RAD', 'CKO', 'SIK'
];

const initialValues = {
  sem1: 3.0,
  sem2: 3.0,
  sem3: 3.0,
  programStudi: programStudiOptions[0],
  kodeDosen: kodeDosenOptions[0]
};

const Prediction = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const onFinish = async (values) => {
    setLoading(true);
    try {
      const result = await predictGraduation(values);
      navigate('/result', { state: { ...values, ...result } });
    } catch (err) {
      message.error('Prediction failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="prediction-bg" style={{ backgroundImage: `url(${bg})` }}>
      <div className="prediction-form-container">
        <h2 className="prediction-title">Enter Your Academic Details</h2>
        <Form
          layout="vertical"
          initialValues={initialValues}
          onFinish={onFinish}
          className="prediction-form"
        >
          <Row gutter={32}>
            <Col xs={24} md={12}>
              <Form.Item 
                label="Semester 1 IPS" 
                name="sem1" 
                rules={[{ required: true, message: 'Please input your Semester 1 IPS' }]}
              >
                <InputNumber min={0} max={4} step={0.01} style={{ width: '100%' }} />
              </Form.Item>
              <Form.Item 
                label="Semester 2 IPS" 
                name="sem2" 
                rules={[{ required: true, message: 'Please input your Semester 2 IPS' }]}
              >
                <InputNumber min={0} max={4} step={0.01} style={{ width: '100%' }} />
              </Form.Item>
              <Form.Item 
                label="Semester 3 IPS" 
                name="sem3" 
                rules={[{ required: true, message: 'Please input your Semester 3 IPS' }]}
              >
                <InputNumber min={0} max={4} step={0.01} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item 
                label="Program Studi" 
                name="programStudi" 
                rules={[{ required: true, message: 'Please select your Program Studi' }]}
              >
                <Select>
                  {programStudiOptions.map(option => (
                    <Option key={option} value={option}>{option}</Option>
                  ))}
                </Select>
              </Form.Item>
              <Form.Item 
                label="Kode Dosen" 
                name="kodeDosen" 
                rules={[{ required: true, message: 'Please select your Dosen Wali' }]}
              >
                <Select>
                  {kodeDosenOptions.map(option => (
                    <Option key={option} value={option}>{option}</Option>
                  ))}
                </Select>
              </Form.Item>
            </Col>
          </Row>
          <div className="prediction-btn-row">
            <Button type="primary" htmlType="submit" size="large" className="prediction-btn" block disabled={loading}>
              {loading ? <Spin /> : 'PREDICT'}
            </Button>
          </div>
        </Form>
        <img src={graduateCharacter} alt="Graduate Character" className="prediction-character" />
      </div>
    </div>
  );
};

export default Prediction; 