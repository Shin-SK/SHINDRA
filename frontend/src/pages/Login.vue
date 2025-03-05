<template>
	<div class="container">
	  <h2>ログイン</h2>
	  <form @submit.prevent="login">
		<div>
		  <label>Username:</label>
		  <input v-model="username" type="text" required />
		</div>
		<div>
		  <label>Password:</label>
		  <input v-model="password" type="password" required />
		</div>
		<button type="submit" :disabled="loading">ログイン</button>
	  </form>
	</div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import api from '@/api'  // 先ほどの api.js
  
  const router = useRouter()
  
  const username = ref('')
  const password = ref('')
  const loading = ref(false)
  
  async function login() {
	loading.value = true
	try {
	  // Django側のURL: /api/auth/login/ に POST
	  const response = await api.post('auth/login/', {
		username: username.value,
		password: password.value
	  })
  
	  // レスポンスからトークンを取り出す
	  const { access, refresh } = response.data
  
	  // ローカルストレージに保存
	  localStorage.setItem('accessToken', access)
	  localStorage.setItem('refreshToken', refresh)
  
	  // 以降のAPIリクエストにトークンを付ける
	  api.defaults.headers.common['Authorization'] = `Bearer ${access}`
  
	  alert('ログイン成功!')
  
	  // ログイン後ダッシュボードへ移動
	  router.push('/dashboard')
	} catch (error) {
	  console.error('ログインエラー:', error)
	  alert('ログインに失敗しました…')
	} finally {
	  loading.value = false
	}
  }
  </script>
  