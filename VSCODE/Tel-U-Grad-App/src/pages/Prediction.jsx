import React, { useState } from 'react';
import { Form, InputNumber, Select, Button, Row, Col, message, Spin, Radio } from 'antd';
import { useNavigate } from 'react-router-dom';
import { predictGraduation } from '../api/prediction';
import graduateCharacter from '../assets/Graduate Character.png';
import bg from '../assets/bg.jpg';
import './Prediction.css';

const { Option } = Select;

const programStudiDisplayMap = [
  { display: 'D3 Teknik Telekomunikasi', value: 'D3 Teknik Telekomunikasi' },
  { display: 'S1 Teknik Telekomunikasi', value: 'S1 Teknik Telekomunikasi' },
  { display: 'S1 Teknik Elektro', value: 'S1 Teknik Elektro' },
  { display: 'S1 Teknik Biomedis', value: 'S1 Teknik Biomedis' },
  { display: 'S1 Teknologi Pangan', value: 'S1 Teknologi Pangan' },
  { display: 'S1 Bisnis Digital', value: 'S1 Bisnis Digital' },
  { display: 'S1 Desain Komunikasi Visual', value: 'S1 Desain Komunikasi Visual' },
  { display: 'S1 Teknik Industri', value: 'S1 Teknik Industri' },
  { display: 'S1 Teknik Logistik', value: 'S1 Teknik Logistik' },
  { display: 'S1 Desain Produk', value: 'S1 Desain Produk' },
  { display: 'S1 Teknik Informatika', value: 'S1 Teknik Informatika - Kampus Purwokerto' },
  { display: 'S1 Sains Data', value: 'S1 Sains Data - Kampus Purwokerto' },
  { display: 'S1 Rekayasa Perangkat Lunak', value: 'S1 Rekayasa Perangkat Lunak - Kampus Purwokerto' },
  { display: 'S1 Sistem Informasi', value: 'S1 Sistem Informasi - Kampus Purwokerto' }
];
const originalProgramStudi = [
  'S1 Teknik Informatika - Kampus Purwokerto',
  'S1 Sistem Informasi - Kampus Purwokerto',
  'S1 Rekayasa Perangkat Lunak - Kampus Purwokerto',
  'S1 Sains Data - Kampus Purwokerto'
];

const initialValues = {
  sem1: 3.0,
  sem2: 3.0,
  sem3: 3.0,
  sem4: 3.0,
  gender: 'Laki-laki',
  programStudi: programStudiDisplayMap[0].value
};

const Prediction = () => {
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const [selectedProgram, setSelectedProgram] = useState(programStudiDisplayMap[0].value);

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
                // rules={[{ required: true, message: 'Please input your Semester 1 IPS' }]}
              >
                <InputNumber min={0} max={4} step={0.01} style={{ width: '100%' }} />
              </Form.Item>
              <Form.Item 
                label="Semester 2 IPS" 
                name="sem2" 
                // rules={[{ required: true, message: 'Please input your Semester 2 IPS' }]}
              >
                <InputNumber min={0} max={4} step={0.01} style={{ width: '100%' }} />
              </Form.Item>
              <Form.Item 
                label="Semester 3 IPS" 
                name="sem3" 
                // rules={[{ required: true, message: 'Please input your Semester 3 IPS' }]}
              >
                <InputNumber min={0} max={4} step={0.01} style={{ width: '100%' }} />
              </Form.Item>
              <Form.Item 
                label="Semester 4 IPS" 
                name="sem4" 
                // rules={[{ required: true, message: 'Please input your Semester 4 IPS' }]}
              >
                <InputNumber min={0} max={4} step={0.01} style={{ width: '100%' }} />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item 
                label="Gender" 
                name="gender" 
                rules={[{ required: true, message: 'Please select your gender' }]}
              >
                <Radio.Group>
                  <Radio value="Laki-laki" style={{ color: 'white' }}>Laki-laki</Radio>
                  <Radio value="Perempuan" style={{ color: 'white' }}>Perempuan</Radio>
                </Radio.Group>
              </Form.Item>
              <Form.Item 
                label="Program Studi" 
                name="programStudi" 
                rules={[{ required: true, message: 'Please select your Program Studi' }]}
              >
                <Select onChange={value => setSelectedProgram(value)}>
                  {programStudiDisplayMap.map(option => (
                    <Option key={option.value} value={option.value}>{option.display}</Option>
                  ))}
                </Select>
              </Form.Item>
              {!originalProgramStudi.includes(selectedProgram) && (
                <div style={{
                  fontSize: '0.75rem',
                  color: 'white',
                  fontWeight: 'bold',
                  marginTop: -12,
                  marginBottom: 12
                }}>
                  Prediksi untuk program studi ini menggunakan model generalisasi dari 4 Program Studi: S1 Teknik Informatika, S1 Sistem Informasi, S1 Rekayasa Perangkat Lunak, dan S1 Sains Data, sehingga hasil prediksi tidak cukup akurat pada program studi lainnya.
                </div>
              )}
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