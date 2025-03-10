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
  
	// 1) ２つの props を受け取る
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
  
	setup(props) {
	  const isFavorited = ref(false)
  
	  // 2) onMountedで slug で投稿詳細をGET → is_favoritedを取得
	  onMounted(async () => {
		try {
		  const postRes = await api.get(`posts/${props.postSlug}/`)  
		  // ここでレスポンスから is_favorited を取得（slugを使う）
		  isFavorited.value = postRes.data.is_favorited
		} catch (error) {
		  console.error('投稿詳細の取得エラー:', error)
		}
	  })
  
	  // 3) toggleFavorite では ID ベースでお気に入り登録/解除
	  const toggleFavorite = async () => {
		try {
		  const response = await api.post(`favorites/${props.postId}/`)
		  if (response.status === 201) {
			isFavorited.value = true
		  } else if (response.status === 204) {
			isFavorited.value = false
		  }
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
  