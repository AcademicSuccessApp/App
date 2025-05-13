import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ConfigProvider, Layout } from 'antd';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Services from './pages/Services';
import Prediction from './pages/Prediction';
import Result from './pages/Result';
import About from './pages/About';
import HowItWorks from './pages/HowItWorks';
import Contact from './pages/Contact';
import './App.css';

const { Content, Footer } = Layout;

function App() {
  return (
    <ConfigProvider theme={{ token: { colorPrimary: '#F44336' } }}>
      <Router>
        <Layout style={{ minHeight: '100vh', background: '#fff' }}>
          <Navbar />
          <Content style={{ flex: 1 }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/services" element={<Services />} />
              <Route path="/predict" element={<Prediction />} />
              <Route path="/result" element={<Result />} />
              <Route path="/about" element={<About />} />
              <Route path="/how-it-works" element={<HowItWorks />} />
              <Route path="/contact" element={<Contact />} />
            </Routes>
          </Content>
          <Footer style={{ textAlign: 'center', background: '#fff' }}>
            © 2024 Tel-U GRAD. All rights reserved.
          </Footer>
        </Layout>
      </Router>
    </ConfigProvider>
  );
}

export default App;
