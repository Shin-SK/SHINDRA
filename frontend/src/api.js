import axios from 'axios';

const accessToken = localStorage.getItem('accessToken') || ""

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: {
    'Content-Type': 'application/json',
    // 初回ロード時にトークンがあれば付ける
    'Authorization': accessToken ? `Bearer ${accessToken}` : ''
  }
});

export default api;
