<template>
	<div class="setting form">
	  <div class="area user-form">
		<!-- ユーザー名更新フォーム -->
		<form @submit.prevent="updateUsername" class="form__wrap">
		  <h2>ユーザー名変更</h2>
		  <input v-model="username" type="text" placeholder="New Username" />
		  <button type="submit">変更</button>
		</form>
	  </div>
	  
	  <div class="area email-form">
		<!-- メールアドレス更新フォーム -->
		<form @submit.prevent="updateEmail" class="form__wrap">
		  <h2>メールアドレス変更</h2>
		  <input v-model="email" type="email" placeholder="New Email" />
		  <button type="submit">変更</button>
		</form>
	  </div>
  
	  <div class="area pw-reset">
		<form @submit.prevent="changePassword" class="form__wrap">
			<h2>パスワード変更</h2>
			<div class="area">
				<input v-model="oldPassword" type="password" required placeholder="現在のパスワード" />
				<input v-model="newPassword1" type="password" required placeholder="新しいパスワード" />
				<input v-model="newPassword2" type="password" required placeholder="新しいパスワード(再入力)" />
				<button type="submit" :disabled="loading">変更</button>
			</div>
		</form>
	  </div>

	  <div class="area contact">
		<h2>Contact</h2>
		<p>お困りの際は、instagramのDMへ</p>
		<a href="http://instagram.com/shinkoyanagi004/" target="_blank"><i class="fab fa-instagram"></i></a>
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
  import api from '@/api'
  
  const email = ref('')
  const username = ref('')
  const message = ref('')
  
  // パスワード変更用
  const oldPassword = ref('')
  const newPassword1 = ref('')
  const newPassword2 = ref('')
  const loading = ref(false)
  
  // エラー・成功メッセージ表示用
  const errorMessage = ref(null)
  const successMessage = ref('')
  
  async function updateUsername() {
	try {
	  await api.patch('dj-rest-auth/user/', {
		username: username.value
	  })
	  successMessage.value = "ユーザー名を変更しました"
	  errorMessage.value = null
	} catch (err) {
	  console.error(err)
	  successMessage.value = ''
	  errorMessage.value = err.response?.data || { detail: 'エラーが発生しました' }
	}
  }
  
  async function updateEmail() {
	try {
	  await api.patch('dj-rest-auth/user/', {
		email: email.value
	  })
	  successMessage.value = "メールを変更しました"
	  errorMessage.value = null
	} catch (err) {
	  console.error(err)
	  successMessage.value = ''
	  errorMessage.value = err.response?.data || { detail: 'エラーが発生しました' }
	}
  }
  
  // パスワード変更
  async function changePassword() {
	loading.value = true
	errorMessage.value = null
	successMessage.value = ''
	try {
	  await api.post('dj-rest-auth/password/change/', {
		old_password: oldPassword.value,
		new_password1: newPassword1.value,
		new_password2: newPassword2.value
	  })
	  successMessage.value = 'パスワードを変更しました'
	  // 入力フィールドをリセット
	  oldPassword.value = ''
	  newPassword1.value = ''
	  newPassword2.value = ''
	} catch (err) {
	  console.error(err)
	  errorMessage.value = err.response?.data || { detail: 'エラーが発生しました' }
	} finally {
	  loading.value = false
	}
  }
  </script>
  