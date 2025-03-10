<template>
	<div class="base-layout container-fluid">
  
	  <!-- メインコンテンツ（PostList, PostDetail, etc）を差し込む場所 -->
	  <router-view />
  
	  <!-- フッター or フッターボタンなど共通表示 -->
	  <FooterButton />
	</div>
  </template>
  
  <script>
  import FooterButton from '@/components/FooterButton.vue'
  
  export default {
	name: 'BaseLayout',
	components: {
	  FooterButton
	}
  }
  </script>
  