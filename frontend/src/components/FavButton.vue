<template>
	<div class="fav-button">
	  <button @click="toggleFavorite">
		<span class="fav" :class="{ active: isFavorited }"></span>
	  </button>
	</div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue'
  import api from '@/api'
  
  export default {
	name: 'FavButton',
  
	props: {
	  postId: {
		type: Number,
		required: true
	  },
	  postSlug: {
		type: String,
		required: true
	  }
	},
  
	setup(props, { emit }) {
	  const isFavorited = ref(false)
  
	  // 投稿詳細を取得して、初期の「お気に入り状態」を反映
	  onMounted(async () => {
		try {
		  const postRes = await api.get(`posts/${props.postSlug}/`)
		  isFavorited.value = postRes.data.is_favorited
		} catch (error) {
		  console.error('投稿詳細の取得エラー:', error)
		}
	  })
  
	  // お気に入り登録／解除
	  const toggleFavorite = async () => {
		try {
		  const response = await api.post(`favorites/${props.postId}/`)
		  if (response.status === 201) {
			// 新規登録
			isFavorited.value = true
		  } else if (response.status === 204) {
			// 解除
			isFavorited.value = false
		  }
		  // ★ ここで親に通知 → 「お気に入りが更新されたよ」
		  emit('favorite-updated')
		} catch (error) {
		  if (error.response && error.response.status === 401) {
			alert('ログインしてください')
		  } else {
			console.error('お気に入り操作エラー:', error)
		  }
		}
	  }
  
	  return {
		isFavorited,
		toggleFavorite
	  }
	}
  }
  </script>