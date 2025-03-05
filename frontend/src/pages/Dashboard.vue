<template>
	<div class="dashboard container">
		<h2>DASHBOARD</h2>

		<div class="favorite--list">
		<h4>お気に入り</h4>
		<!-- グリッド -->
		<div class="area grid-4">
			<div class="box" v-for="post in filteredPosts" :key="post.id">
			<!-- 画像リンク -->
			<router-link :to="`/posts/${post.slug}`" class="tumbnail">
				<img v-if="post.image" :src="post.image" alt="投稿画像" />
				<img v-else src="/dummy.webp" alt="ダミー画像" />
			</router-link>

			<!-- タイトルリンク -->
			<router-link :to="`/posts/${post.slug}`">
				<h3>{{ post.title }}</h3>
			</router-link>

			<!-- タグ表示（お好みで対応） -->
			<div class="tags">
				<span v-for="tag in (post.tags || [])" :key="tag.id">#{{ tag.name }}</span>
			</div>
			</div>
		</div><!-- area -->
				<div class="allpost">
			<router-link :to="`/posts/`">allpost</router-link>
		</div>
		</div><!-- favList -->

		<div class="history">
		<h4>最近見た投稿</h4>
		<div class="area grid-4 container">
			<div class="box" v-for="item in viewHistory" :key="item.id">
			<!-- 画像リンク -->
			<router-link :to="`/posts/${item.slug}`" class="tumbnail">
				<img v-if="item.image" :src="item.image" alt="投稿画像" />
				<img v-else src="/dummy.webp" alt="ダミー画像" />
			</router-link>
			<router-link :to="`/posts/${item.slug}`">
				<h3>{{ item.title }}</h3>
			</router-link>
			</div>
		</div>
		</div>
	</div>
</template>
  
  <script>
  import { ref, onMounted, computed } from 'vue'
  import api from '@/api'
  
  export default {
	name: 'Dashboard',
	setup() {
	  const favoritePosts = ref([])
	  const viewHistory = ref([])
  
	  onMounted(async () => {
		try {
		  // ローカルストレージから閲覧履歴を読み込む
		  const historyStr = localStorage.getItem('viewHistory') || '[]'
		  viewHistory.value = JSON.parse(historyStr)
  
		  // /api/favorites/ でお気に入り一覧を取得 (要ログイン)
		  const res = await api.get('favorites/')
		  // 返ってくるのが [ { id, user, post: {...} }, ... ] の想定
		  // → fav.post を配列に格納
		  favoritePosts.value = res.data.map(fav => fav.post)
		} catch (error) {
		  console.error('お気に入り取得エラー:', error)
		}
	  })
  
	  // お気に入りをそのまま返すだけ
	  const filteredPosts = computed(() => favoritePosts.value)

	  return {
		favoritePosts,
		filteredPosts,
		viewHistory // ← ここを忘れずに返す
	  }
	}
  }
  </script>
  