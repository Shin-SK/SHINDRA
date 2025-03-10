<template>
	<div class="form login">
	  <form @submit.prevent="login" class="form__wrap">
		<div class="area">
			<input v-model="username" required placeholder="USERNAME" autocapitalize="none" autocomplete="off" autocorrect="off" />
			<input v-model="password" type="password" placeholder="PASSWORD" autocapitalize="none" autocomplete="off" autocorrect="off" />
			<button type="submit"><img src="@/assets/image/icon.svg" alt="">LOGIN</button>
		</div><!-- area -->
		<div class="area">
			<router-link to="/signup">SIGNUP</router-link>
		</div>
	  </form>
	</div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import api from '@/api'  // あなたの api.js を import
  import { useRouter } from 'vue-router'
  
  const router = useRouter()
  
  const username = ref('')
  const password = ref('')
  
  async function login() {
	try {
	  // 1) 古いキーを掃除する（JWT残骸など）
	  localStorage.removeItem('accessToken')
	  localStorage.removeItem('refreshToken')
	  localStorage.removeItem('token')
	  // もし "user" キーに古いデータがあるなら削除
	  localStorage.removeItem('user')
	  localStorage.removeItem('authToken')
  
	  // 2) dj-rest-auth で「Tokenログイン」
	  //    通常レスポンス: { key: "4f3a70db..." }
	  const response = await api.post('dj-rest-auth/login/', {
		username: username.value,
		password: password.value
	  })
	  
	  // 3) authToken をローカルストレージに保存
	  const key = response.data.key // { key: "xxxxxx" }
	  localStorage.setItem('authToken', key)
	  // 以後のAPIリクエストに付与する
	  api.defaults.headers.common['Authorization'] = `Token ${key}`
  
	  // 4) ログインしたユーザー情報を再取得（dj-rest-auth が提供する /user/ へGET）
	  //    これを呼び出すと { pk, username, email, ... } が返ってくる
	  //    endpoint: /api/dj-rest-auth/user/ (デフォルトURL)
	  const meRes = await api.get('dj-rest-auth/user/')
	  // 例: { pk: 123, username: "public-user", email: "..." }
	  const userData = meRes.data
	  localStorage.setItem('user', JSON.stringify(userData))
  
	  // 完了メッセージ & 画面遷移
	  alert("ログイン完了: " + userData.username)
	  router.push('/dashboard')
	  
	} catch (error) {
	  console.error("ログインエラー:", error)
	  alert("ログインに失敗しました…")
	}
  }
  </script>
  