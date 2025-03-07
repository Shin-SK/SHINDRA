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
  import { ref } from "vue";
  import api from "@/api"; // ★ import api(認証付き)
  
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
		  // ★ ここで api.post → ユーザー認証付きリクエスト
		  const response = await api.post(`payments/${props.postId}/`, {
			amount: amount.value, // (数値)
		  });
  
		  // Stripe決済URLが { url: "https://checkout.stripe.com/..." } で返る想定
		  if (response.data.url) {
			window.location.href = response.data.url;
		  } else {
			console.warn("Stripe URLが返されませんでした:", response.data);
		  }
		} catch (err) {
		  console.error("投げ銭エラー:", err);
		  alert("投げ銭に失敗しました…");
		} finally {
		  loading.value = false;
		}
	  };
  
	  return { donate, loading, amount };
	},
  };
  </script>
  