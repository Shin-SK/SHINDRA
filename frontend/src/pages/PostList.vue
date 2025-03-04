<template>
	<div class="posts posts--list story container-fluid">
	  <h2>POSTS</h2>
  
	  <div class="search container">
		<input v-model="searchTerm" placeholder="タイトル検索" />
	  </div>
  
	  <div class="filter container">
		<div class="wrap cat">
		  <span 
			v-for="cat in categories" 
			:key="cat.id" 
			@click="filterByCategory(cat.slug)"
			:class="{ selected: selectedCategory === cat.slug }"
		  >
			{{ cat.name }}
		  </span>
		  <button @click="clearCategory">全て</button>
		</div>
		<div class="wrap tag">
		  <span 
			v-for="tag in tags" 
			:key="tag.id" 
			@click="filterByTag(tag.slug)"
			:class="{ selected: selectedTag === tag.slug }"
		  >
			#{{ tag.name }}
		  </span>
		  <button @click="clearTag">全て</button>
		</div>
	  </div>
  
	  <!-- グリッド全体を <transition> でラップ -->
	  <transition mode="out-in" name="fade">
		<div :key="gridKey" class="area container">
		  <div class="box" v-for="post in filteredPosts" :key="post.id">
			<!-- 画像リンク -->
			<router-link :to="`/posts/${post.slug}`" class="tumbnail">
			  <img v-if="post.image" :src="post.image" alt="投稿画像" />
			  <img v-else src="/dummy.webp" alt="ダミー画像" />
			</router-link>
  
			<!-- タイトルリンク -->
			<router-link :to="`/storys/${post.slug}`">
			  <h3>{{ post.title }}</h3>
			</router-link>
  
			<!-- タグ表示 -->
			<div class="tags">
			  <span v-for="tag in tags" :key="tag">#{{ tag.name }}</span>
			</div>
		  </div>
		</div>
	  </transition>
	</div>
  </template>
  
  <script>
  import { ref, onMounted, computed } from 'vue';
  import { useRouter, useRoute } from 'vue-router';
  import api from '@/api';
  
  export default {
	setup() {
	  const posts = ref([]);
	  const categories = ref([]);
	  const tags = ref([]);
	  const searchTerm = ref('');
	  const selectedCategory = ref('');
	  const selectedTag = ref(null);
	  const router = useRouter();
	  const route = useRoute();
  
	  onMounted(async () => {
		try {
		  const postsResponse = await api.get('posts/');
		  posts.value = postsResponse.data;
		  const categoriesResponse = await api.get('posts/categories/');
		  categories.value = categoriesResponse.data;
		  const tagsResponse = await api.get('posts/tags/');
		  tags.value = tagsResponse.data;
	
		  if (route.query.category) {
			selectedCategory.value = route.query.category;
		  }
		} catch (error) {
		  console.error('API取得エラー:', error);
		}
	  });
  
	  const filterByCategory = (slug) => {
		selectedCategory.value = slug;
	  };
  
	  const filterByTag = (slug) => {
		selectedTag.value = slug;
	  };
  
	  const clearCategory = () => {
		selectedCategory.value = '';
	  };
  
	  const clearTag = () => {
		selectedTag.value = null;
	  };
  
	  const filteredPosts = computed(() => {
		return posts.value.filter(post => {
		  const matchTitle = post.title.toLowerCase().includes(searchTerm.value.toLowerCase());
		  const matchCategory = selectedCategory.value ? post.category_slug === selectedCategory.value : true;
		  const matchTag = selectedTag.value !== null ? post.tag_slugs.includes(selectedTag.value) : true;
		  return matchTitle && matchCategory && matchTag;
		});
	  });
  
	  // グリッドのキーはフィルター条件が変わるたびに変える
	  const gridKey = computed(() => {
		return `${selectedCategory.value}-${selectedTag.value}-${searchTerm.value}`;
	  });
  
	  return {
		posts,
		categories,
		tags,
		searchTerm,
		filteredPosts,
		filterByCategory,
		filterByTag,
		clearCategory,
		clearTag,
		router,
		selectedCategory,
		selectedTag,
		gridKey,
	  };
	},
  };
  </script>
  
  <style scoped>
  .fade-enter-active,
  .fade-leave-active {
	transition: opacity 0.3s ease;
  }
  .fade-enter-from,
  .fade-leave-to {
	opacity: 0;
  }
  </style>
  