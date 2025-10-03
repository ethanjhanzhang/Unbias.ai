import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001';

export const analyzePrompt = async (prompt, mode = 'nlp') => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/analyze`, {
      prompt,
      mode
    });
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.error || 'Failed to analyze prompt'
    );
  }
};

export const detectBias = async (prompt) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/api/detect`, {
      prompt
    });
    return response.data;
  } catch (error) {
    throw new Error(
      error.response?.data?.error || 'Failed to detect bias'
    );
  }
};
