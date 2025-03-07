<template>
	<div class="posts--podcast">
	  <div class="area">
		<!-- たとえばPodcast用の表示、あるいはYouTube iframe埋め込みなど -->
		<div class="contents" v-html="convertedHtml"></div>
	  </div>
	  <div class="share">
		<ShareButton :title="post.title" />
	  </div>
	  <div class="donate">
		<DonateButton v-if="post.id" :postId="post.id" />
	  </div>
	</div>
  </template>
  
  <script setup>
  import { defineProps, computed } from 'vue'
  import { convertYoutubeLinksToIframe } from '@/utils/youtubeTransform.js'
  
  const props = defineProps({
	post: {
	  type: Object,
	  required: true
	}
  })
  
  const convertedHtml = computed(() => {
	// ここでは post.content を iframe に変換する例
	return convertYoutubeLinksToIframe(props.post.content)
  })
  </script>
  