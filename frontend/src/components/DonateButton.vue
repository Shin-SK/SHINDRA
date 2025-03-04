<template>
	<div class="donate--button">
	  <input
		type="number"
		v-model="amount"
		placeholder="お気持ちで結構です"
		min="100"
		max="50000"
	  />
	  <button @click="donate" class="donate-button" :disabled="loading">
		{{ loading ? "処理中..." : "投げ銭" }}
	  </button>
	</div>
  </template>
  
  <script>
  import axios from "axios";
  import { ref } from "vue";
  
  export default {
	props: {
	  postId: {
		type: Number,
		required: true,
	  },
	},
	setup(props) {
	  const loading = ref(false);
	  const amount = ref("");
  
	  const donate = async () => {
		if (!amount.value) {
		  alert("金額を入力してください。");
		  return;
		}
		loading.value = true;
		try {
		  const response = await axios.post(
			`${import.meta.env.VITE_API_BASE_URL}payments/${props.postId}/`,
			{ amount: amount.value }
		  );
		  if (response.data.url) {
			window.location.href = response.data.url;
		  }
		} catch (err) {
		  console.error("投げ銭エラー:", err);
		} finally {
		  loading.value = false;
		}
	  };
  
	  return { donate, loading, amount };
	},
  };
  </script>
  