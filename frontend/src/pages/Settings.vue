<template>
	<div class="setting form">
		<div class="pw-reset">
			<h2>パスワード変更</h2>
			<form @submit.prevent="changePassword" class="form__wrap">
				<div class="area">
					<input v-model="oldPassword" type="password" required placeholder="現在のパスワード"/>
					<input v-model="newPassword1" type="password" required placeholder="新しいパスワード"/>
					<input v-model="newPassword2" type="password" required placeholder="新しいパスワード(再入力)" />
					<button type="submit" :disabled="loading">変更</button>
				</div>
			</form>
		</div>

	  <div class="error" v-if="errorMessage">
		<!-- エラーメッセージを表示 -->
		<p v-for="(msgs, field) in errorMessage" :key="field">
		  <strong>{{ field }}: </strong>
		  <!-- msgs が配列の場合まとめて出力 -->
		  <span v-if="Array.isArray(msgs)">{{ msgs.join(" / ") }}</span>
		  <span v-else>{{ msgs }}</span>
		</p>
	  </div>
  
	  <div class="success" v-if="successMessage">
		<p>{{ successMessage }}</p>
	  </div>
	</div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import api from '@/api'     // 既存の axiosインスタンス (Token認証 などが付与済み)
  
  const oldPassword = ref('')
  const newPassword1 = ref('')
  const newPassword2 = ref('')
  const loading = ref(false)
  
  // エラー・成功メッセージ
  const errorMessage = ref(null)
  const successMessage = ref('')
  
  async function changePassword() {
	loading.value = true
	errorMessage.value = null
	successMessage.value = ''
  
	try {
	  // dj-rest-auth公式: 
	  // POST /dj-rest-auth/password/change/
	  // { old_password, new_password1, new_password2 }
	  const response = await api.post('dj-rest-auth/password/change/', {
		old_password: oldPassword.value,
		new_password1: newPassword1.value,
		new_password2: newPassword2.value
	  })
	  console.log('パスワード変更レスポンス:', response.data)
  
	  // 成功時
	  successMessage.value = 'パスワードを変更しました！'
	  // フォームをリセット
	  oldPassword.value = ''
	  newPassword1.value = ''
	  newPassword2.value = ''
	} catch (error) {
	  console.error('パスワード変更エラー:', error.response?.data)
	  // エラー内容を画面表示用に格納
	  if (error.response?.data) {
		errorMessage.value = error.response.data
	  } else {
		errorMessage.value = { detail: 'エラーが発生しました' }
	  }
	} finally {
	  loading.value = false
	}
  }
  </script>
  
  <style scoped>
  .container {
	max-width: 400px;
	margin: 0 auto;
  }
  .error {
	margin-top: 1rem;
	color: red;
  }
  .success {
	margin-top: 1rem;
	color: green;
  }
  </style>
  