// src/api.js
import axios from 'axios'

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  headers: {
    'Content-Type': 'application/json'
  }
})

// リクエストインターセプター
api.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken') || ""
  if (token) {
    config.headers.Authorization = `Token ${token}`
  } else {
    delete config.headers.Authorization
  }
  return config
})

export default api
