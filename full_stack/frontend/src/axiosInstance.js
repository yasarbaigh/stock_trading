
import axios from 'axios';

const axiosInstance = axios.create({

  baseURL: process.env.VUE_APP_API_BASE_URL, // Vite reads the environment variable
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;
