<template>

	<!-- <h2>COMMENT</h2> -->

	<div class="share-button">
	  <i class="fab fa-twitter" @click="shareOnTwitter"></i>
	  <!-- <a href="https://open.spotify.com/show/6nGIbhu2abuqZrzXR4JHKJ?si=H1x7Di-_SBWEqWilaTO3zw"><i class="fab fa-spotify"></i></a> -->
	</div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue'
import FavButton from './FavButton.vue'
  
  // タイトルのみ受け取る
  const props = defineProps({
	title: {
	  type: String,
	  required: true
	}
  })
  
  // クリックしたらツイート画面を開く
  function shareOnTwitter() {
	const text = `『${props.title}』\n`
	const url = window.location.href
	window.open(
	  `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`,
	  '_blank'
	)
  }
  </script>
  