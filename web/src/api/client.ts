import axios from 'axios';

const client = axios.create({
  baseURL: __API_BASE__,
  withCredentials: true,
});

client.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.warn('Authentication required');
    }
    return Promise.reject(error);
  }
);

export default client;
