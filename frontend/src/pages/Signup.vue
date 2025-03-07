<template>
	<div class="form signup">
	  <form @submit.prevent="signup" class="form__wrap">
		<div class="area">
			<input v-model="username" type="text" required placeholder="USERNAME"/>
			<input v-model="email" type="email" required placeholder="EMAIL"/>
			<input v-model="password1" type="password" required placeholder="PASSWORD"/>
			<input v-model="password2" type="password" required placeholder="CONFIRM PW"/>
			<button type="submit">SIGNUP</button>
		</div>
	  </form>
  
	  <!-- エラー表示 -->
	  <div class="error" v-if="errorMessage">
		<!-- 例: { username: ["このフィールドは必須です"], ... } -->
		<p
		  v-for="(messages, fieldName) in errorMessage"
		  :key="fieldName"
		>
		  <!-- 配列かどうか判定しつつ、各メッセージを翻訳 -->
		  <span v-if="Array.isArray(messages)">
			{{ messages.map(msg => translateError(msg)).join(' / ') }}
		  </span>
		  <span v-else>
			{{ translateError(messages) }}
		  </span>
		</p>
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
  
  // 1) エラーメッセージ辞書 (英語 or 既定文言 → 好みの日本語に)
  const errorMapping = {
	"Enter a valid email address.": "正しいメールアドレスを入力してください。",
	"This password is too short. It must contain at least 8 characters.":
	  "パスワードが短すぎます（8文字以上にしてください）",
	"This password is too common.": "パスワードが簡単すぎます",
	"A user is already registered with this e-mail address.":"そのメアドは誰かに使われてるぜ",
	// 必要に応じて追加...
  }
  
  // 2) メッセージ翻訳関数
  function translateError(originalMsg) {
	// マップにあれば置き換え、無ければそのまま
	return errorMapping[originalMsg] || originalMsg
  }
  
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
  .container {
	max-width: 400px;
	margin: 0 auto;
  }
  .error {
	margin-top: 1rem;
	color: red;
  }
  </style>
  