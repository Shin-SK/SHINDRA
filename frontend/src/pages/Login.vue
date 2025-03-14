<template>
	<div class="form login">
	  <form @submit.prevent="login" class="form__wrap">
		<div class="area">
			<input v-model="email" required placeholder="EMAIL" autocapitalize="none" autocomplete="off" autocorrect="off" />
			<input v-model="password" type="password" placeholder="PASSWORD" autocapitalize="none" autocomplete="off" autocorrect="off" />
			<button type="submit"><img src="@/assets/image/icon.svg" alt="">LOGIN</button>
		</div><!-- area -->
		<div class="area signup-button">
			<router-link to="/signup">SIGNUP</router-link>
		</div>
	  </form>
	</div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import api from '@/api'
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  // email 変数を定義
  const email = ref('')
  const password = ref('')
  
  async function login() {
	try {
	  // ローカルストレージ初期化などは省略
	  // メールとパスワードを送信
	  const response = await api.post('dj-rest-auth/login/', {
		email: email.value,
		password: password.value
	  })
  
	  // あとはトークンを保存 & ユーザー情報取得など
	  const key = response.data.key
	  localStorage.setItem('authToken', key)
	  api.defaults.headers.common['Authorization'] = `Token ${key}`
  
	  const meRes = await api.get('dj-rest-auth/user/')
	  const userData = meRes.data
	  localStorage.setItem('user', JSON.stringify(userData))
  
	  alert("ログイン完了: " + userData.email)
	  router.push('/dashboard')
  
	} catch (error) {
	  console.error("ログインエラー:", error)
	  alert("ログインに失敗しました。")
	}
  }
  </script>