import axios from 'axios';

// Mock prediction API
export async function predictGraduation(data) {
  try {
    const response = await axios.post('/api/predict', {
      sem1: data.sem1,
      sem2: data.sem2,
      sem3: data.sem3,
      sem4: data.sem4,
      gender: data.gender,
      programStudi: data.programStudi
    });
    
    return {
      classification: response.data.classification,
      regression: response.data.regression,
      recommendation: response.data.recommendation
    };
  } catch (error) {
    throw new Error('Prediction failed. Please try again.');
  }
} 