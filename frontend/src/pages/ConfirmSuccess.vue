<template>
	<div class="confirm confirm-success">
		<div class="area container">
			<div class="cs-box">
				<h2>メールアドレスの確認ができました</h2>
				<p>ようこそ</p>
			</div>
		</div>
		<div class="cs-outer">
			<Login />
		</div>
	</div>
</template>
  

<script setup>
import { onMounted } from 'vue'
import Login from '@/pages/Login.vue'

// Vue 3 Composition API のマウントフック
onMounted(() => {
  if (typeof window.confetti === 'function') {
    window.confetti();
  }
})

</script>