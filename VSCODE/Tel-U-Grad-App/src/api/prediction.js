import axios from 'axios';

// Mock prediction API
export async function predictGraduation(data) {
  try {
    const response = await axios.post('/api/predict', {
      sem1: data.sem1,
      sem2: data.sem2,
      sem3: data.sem3,
      programStudi: data.programStudi,
      kodeDosen: data.kodeDosen
    });
    
    return {
      probability: response.data.probability,
      status: response.data.status,
      recommendation: response.data.recommendation
    };
  } catch (error) {
    throw new Error('Prediction failed. Please try again.');
  }
} 