<template>
	<div class="posts list story container-fluid">
	  <h1>STORY</h1>
	  <div class="area container">
		<div class="box" v-for="post in posts" :key="post.id">
		  <!-- 画像にリンク -->
		  <router-link :to="`/storys/${post.slug}`" class="image" v-if="post.image">
			<img :src="post.image" alt="投稿画像" />
		  </router-link>
  
		  <!-- タイトルにリンク -->
		  <router-link :to="`/storys/${post.slug}`">
			<h2>{{ post.title }}</h2>
		  </router-link>
  
		  <div class="tags">
			<span v-for="tag in post.tag_slugs" :key="tag">#{{ tag }}</span>
		  </div>
		</div>
	  </div>
	</div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  import { useRouter } from 'vue-router';
  import api from '@/api';
  
  export default {
	setup() {
	  const posts = ref([]);
	  const router = useRouter();
  
	  onMounted(async () => {
		try {
		  const response = await api.get('posts/'); // API からデータ取得
		  posts.value = response.data;
		} catch (error) {
		  console.error('API取得エラー:', error);
		}
	  });
  
	  return { posts, router };
	}
  };
  </script>
  