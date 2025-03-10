<template>
	<div class="form signup">
	  <form @submit.prevent="signup" class="form__wrap">
		<div class="area">
  
		  <!-- ユーザ名 -->
		  <div class="box">
			<input
			  v-model="username"
			  type="text"
			  required
			  placeholder="USERNAME"
			  autocapitalize="none"
			  autocomplete="off"
			  autocorrect="off"
			/>
			<div class="error" v-if="errorMessage && errorMessage.username">
			  <!-- username は配列として返ってくる想定なので v-for で回す -->
			  <p
				v-for="(msg, i) in errorMessage.username"
				:key="i"
			  >
				{{ translateError(msg) }}
			  </p>
			</div>
		  </div>
  
		  <!-- メールアドレス -->
		  <div class="box">
			<input
			  v-model="email"
			  type="email"
			  required
			  placeholder="EMAIL"
			  autocapitalize="none"
			  autocomplete="off"
			  autocorrect="off"
			/>
			<div class="error" v-if="errorMessage && errorMessage.email">
			  <p
				v-for="(msg, i) in errorMessage.email"
				:key="i"
			  >
				{{ translateError(msg) }}
			  </p>
			</div>
		  </div>
  
		  <!-- パスワード1 -->
		  <div class="box">
			<input
			  v-model="password1"
			  type="password"
			  required
			  placeholder="PASSWORD"
			  autocapitalize="none"
			  autocomplete="off"
			  autocorrect="off"
			/>
			<div class="error" v-if="errorMessage && errorMessage.password1">
			  <p
				v-for="(msg, i) in errorMessage.password1"
				:key="i"
			  >
				{{ translateError(msg) }}
			  </p>
			</div>
		  </div>
  
		  <!-- パスワード2 -->
		  <div class="box">
			<input
			  v-model="password2"
			  type="password"
			  required
			  placeholder="CONFIRM PW"
			  autocapitalize="none"
			  autocomplete="off"
			  autocorrect="off"
			/>
			<div class="error" v-if="errorMessage && errorMessage.password2">
			  <p
				v-for="(msg, i) in errorMessage.password2"
				:key="i"
			  >
				{{ translateError(msg) }}
			  </p>
			</div>
		  </div>
  
		  <button type="submit">SIGNUP</button>
		</div>
	  </form>
  
	  <!-- 全体に関わるエラー (detail など) -->
	  <div class="error" v-if="errorMessage && errorMessage.detail">
		<p>{{ translateError(errorMessage.detail) }}</p>
	  </div>
	</div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import api from '@/api'
  
  const router = useRouter()
  
  // ユーザ入力項目
  const username = ref('')
  const email = ref('')
  const password1 = ref('')
  const password2 = ref('')
  
  // エラー表示用
  const errorMessage = ref(null)
  
  // エラーメッセージ辞書
  const errorMapping = {
	"Enter a valid email address.": "正しいメールアドレスを入力してください。",
	"This password is too short. It must contain at least 8 characters.": "パスワードが短すぎます（8文字以上にしてください）",
	"This password is too common.": "パスワードが簡単すぎます",
	"A user is already registered with this e-mail address.": "そのメアドは既に使われています",
	// 必要に応じて追加...
  }
  
  // メッセージ翻訳関数
  function translateError(originalMsg) {
	return errorMapping[originalMsg] || originalMsg
  }
  
  // ユーザ登録処理
  async function signup() {
	try {
	  const response = await api.post('dj-rest-auth/registration/', {
		username: username.value,
		email: email.value,
		password1: password1.value,
		password2: password2.value
	  })
	  console.log('登録成功:', response.data)
	  alert('ユーザー登録が完了しました！')
	  router.push('/login')
	} catch (error) {
	  console.error('登録エラー:', error.response?.data)
	  // APIが返すエラーオブジェクトをそのまま格納
	  // 例: { username: ["このフィールドは必須です。"], email: ["Enter a valid email address."] }
	  if (error.response?.data) {
		errorMessage.value = error.response.data
	  } else {
		errorMessage.value = { detail: ["登録に失敗しました"] }
	  }
	}
  }
  </script>
  
  <style scoped>
  .field-block {
	margin-bottom: 1rem;
  }
  .error {
	margin-top: 0.25rem;
	color: red;
  }
  </style>
  