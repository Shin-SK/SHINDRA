// src/api.js
import axios from 'axios'

// ログイン時に保存した 'authToken'
const token = localStorage.getItem('authToken') || ""

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // ローカル開発用
  headers: {
    'Content-Type': 'application/json',
    // dj-rest-auth なら "Token <キー>"
    'Authorization': token ? `Token ${token}` : ''
  }
})

export default api
