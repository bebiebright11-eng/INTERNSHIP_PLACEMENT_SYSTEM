import axios from 'axios';

const API = axios.create({
    baseURL: 'http://127.0.0.1:8000/api/', // Your Django Server URL
});

// This automatically attaches your Token to every request
API.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Token ${token}`;
    }
    return config;
});

export default API;