<template>
	<div>
	  <button @click="logout"><i class="fas fa-sign-out-alt"></i></button>
	</div>
  </template>
  
  <script setup>
import { useRouter } from 'vue-router'
import api from '@/api'

const router = useRouter()

async function logout() {
  try {
    // サーバ側のセッション・トークンを無効化
    await api.post('/dj-rest-auth/logout/')
  } catch (error) {
    console.error('ログアウトAPIエラー:', error)
    // 必要ならエラーの出し方を調整
  } finally {
    // フロント側トークンも削除
    localStorage.removeItem('authToken')
    // ログイン画面に飛ばす
    router.push({ name: 'login' })
  }
}
</script>