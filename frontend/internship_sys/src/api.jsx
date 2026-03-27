import axios from 'axios';

const API = axios.create({
    // This must match your Django URL exactly
    baseURL: 'http://127.0.0.1:8000/api/', 
    headers: {
        'Content-Type': 'application/json',
    },
});

// This "Interceptor" runs before every request to the backend
API.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        // If we have a token, add it to the 'Authorization' header
        config.headers.Authorization = `Token ${token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

export default API;