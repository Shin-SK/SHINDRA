// src/api.js
import axios from 'axios'
import { useLoadingStore } from '@/stores/loadingStore'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 認証トークン挿入用リクエストインターセプター
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken') || ""
    if (token) {
      config.headers.Authorization = `Token ${token}`
    } else {
      delete config.headers.Authorization
    }

    // ローディングカウント増加
    const loadingStore = useLoadingStore()
    loadingStore.increment()

    return config
  },
  (error) => {
    // リクエスト時に失敗した場合でもローディング数を減らす
    const loadingStore = useLoadingStore()
    loadingStore.decrement()
    return Promise.reject(error)
  }
)

// レスポンスインターセプター
api.interceptors.response.use(
  (response) => {
    // 通信成功時にローディング数を減らす
    const loadingStore = useLoadingStore()
    loadingStore.decrement()
    return response
  },
  (error) => {
    // 通信失敗時にもローディング数を減らす
    const loadingStore = useLoadingStore()
    loadingStore.decrement()
    return Promise.reject(error)
  }
)

// //デザインチェック用
// api.interceptors.response.use(
//   async (response) => {
//     // 通信成功後に人工的な遅延を入れる
//     await new Promise(resolve => setTimeout(resolve, 100000))  // 1000秒待つ
//     const loadingStore = useLoadingStore()
//     loadingStore.decrement()
//     return response
//   },
//   async (error) => {
//     await new Promise(resolve => setTimeout(resolve, 100000))  // 1000秒待つ
//     const loadingStore = useLoadingStore()
//     loadingStore.decrement()
//     return Promise.reject(error)
//   }
// )

export default api
