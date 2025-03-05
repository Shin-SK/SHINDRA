<template>
	<button @click="toggleFavorite">
	  {{ isFavorited ? 'お気に入り解除' : 'お気に入りに追加' }}
	</button>
  </template>
  
  <script>
  import { ref } from 'vue'
  import api from '@/api'
  
  export default {
	name: 'FavButton',
	props: {
	  postId: {
		type: Number,
		required: true
	  }
	},
	setup(props) {
	  const isFavorited = ref(false)
  
	  const toggleFavorite = async () => {
		try {
		  const response = await api.post(
			`${import.meta.env.VITE_API_BASE_URL}favorites/${props.postId}/`
		  )
		  if (response.status === 201) {
			isFavorited.value = true
		  } else if (response.status === 204) {
			isFavorited.value = false
		  }
		} catch (error) {
		  // 401 の場合は未ログイン
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
  