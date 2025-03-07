<template>
	<div class="posts posts--default">
	  <div class="wrap">
		<div class="area">
		  <h1>{{ post.title }}</h1>
		  
		  <div class="contents__story" v-if="post.content_html" v-html="post.content_html"></div>
		  <div class="contents__default" v-else>
			{{ post.content }}
		  </div>
		</div>
		<div class="thumbnail">
		  <img v-if="post.image" :src="post.image" alt="投稿画像" />
		</div>
		<div class="share">
		  <ShareButton :title="post.title"/>
		</div>
		<div class="donate">
		  <DonateButton v-if="post.id" :postId="post.id" />
		</div>
	  </div>
	</div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue'
  import ShareButton from '@/components/ShareButton.vue'
  import DonateButton from '@/components/DonateButton.vue'
  
  // 親から渡される post を表示
  const props = defineProps({
	post: {
	  type: Object,
	  required: true
	}
  })
  
  // onMountedは不要。ここは「表示担当」だけ
  </script>
  