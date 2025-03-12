<template>
	<div class="dashboard posts posts--list">
		<section class="username">
			<div class="username__wrap">
				<span>{{ username }}</span>
			</div>
		</section>
	  <!-- お気に入り一覧 -->
	  <div class="wrap db db--fav">
		<div class="contents-title">LIKE</div>
		<div class="area grid grid--dashboard" v-if="favoritePosts.length > 0">
		  <div class="box" v-for="post in filteredPosts" :key="post.id">
			<!-- 画像リンク -->
			<router-link :to="`/posts/${post.slug}`" class="tumbnail">
			  <img v-if="post.image" v-lazy="post.image" alt="投稿画像" />
			  <img v-else src="/dummy.webp" alt="ダミー画像" />
			</router-link>
			<!-- タイトル -->
			 <div class="title">
				<div class="title__wrap">
					<router-link :to="`/posts/${post.slug}`">
					<h3>{{ post.title }}</h3>
					</router-link>
				</div>
				<!-- お気に入りボタン -->
				<FavButton :postId="post.id" :postSlug="post.slug" />
			 </div>
		  </div>
		</div><!-- /area v-if  -->
		<div class="no-contents" v-else>
			<router-link to="/posts/">いい作品はきっとある</router-link>
		</div>
	  </div>

	  <!-- 閲覧履歴 -->
	  <div class="wrap db db--history">
		<div class="contents-title">HISTORY</div>
		<div class="area grid grid--dashboard" v-if="viewHistory.length > 0">
		  <div class="box" v-for="item in viewHistory" :key="item.id">
			<router-link :to="`/posts/${item.slug}`" class="tumbnail">
			  <img v-if="item.image" v-lazy="item.image" alt="投稿画像" />
			  <img v-else src="/dummy.webp" alt="ダミー画像" />
			</router-link>
			<div class="title">
				<div class="title__wrap">
					<router-link :to="`/posts/${item.slug}`">
					<h3>{{ item.title }}</h3>
					</router-link>
				</div>
			</div>
		  </div>
		</div><!-- /area v-if -->
		<div class="no-contents" v-else>
			<router-link to="/posts/">ひとつくらい読んでほしい</router-link>
		</div>
	  </div>
  
	  <!-- 🔹投げ銭一覧 追加！ -->
	  <div class="wrap db db--donation">
		<div class="contents-title">DONATE</div>
		<div class="area grid grid--dashboard"  v-if="donationHistory.length > 0">
		  <div class="box" v-for="donation in donationHistory" :key="donation.id">
			<!-- 投稿へのリンク -->
			<router-link :to="`/posts/${donation.post_slug}`" class="tumbnail">
			  <img v-if="donation.post_image" v-lazy="donation.post_image" alt="投稿画像" />
			  <img v-else src="/dummy.webp" alt="投稿画像" />
			</router-link>
			<div class="title">
				<div class="title__wrap">
					<router-link :to="`/posts/${donation.post_slug}`">
					<h3>{{ donation.post_title }}</h3>
					</router-link>
					<div class="donate-stamp">{{ donation.amount }} 円</div>
					<div class="time-stamp">{{ formatDateTime(donation.created_at) }}</div>
				</div>
			</div>
		  </div>
		</div><!-- area v-if -->
		<div class="no-contents" v-else>
			<router-link to="/posts/">愛顧のお陰で書けてます</router-link>
		</div>
	  </div>
	</div>
  </template>
  
  <script>
  import { ref, onMounted, computed } from 'vue'
  import api from '@/api'
  import TagLinks from '@/components/TagLinks.vue'
  import { formatDateTime } from '@/utils/dateFormat.js'

  
  export default {
	name: 'Dashboard',
	components: { TagLinks },
	setup() {
		// ユーザーネーム用
		const username = ref('')
		// ふぁぼ
		const favoritePosts = ref([])
		// 視聴履歴
		const viewHistory = ref([])
	  // 投げ銭
	  const donationHistory = ref([])

	  onMounted(async () => {
		try {
			//ユーザ系
			const userRes = await api.get('users/')
			username.value = userRes.data.username

			// 閲覧履歴
			const historyStr = localStorage.getItem('viewHistory') || '[]'
			viewHistory.value = JSON.parse(historyStr)
  
		  // お気に入り一覧
		  const favRes = await api.get('favorites/')
		  favoritePosts.value = favRes.data.map(fav => fav.post)
  
		  // 投げ銭履歴
		  const donationRes = await api.get('payments/history/')
		  donationHistory.value = donationRes.data
		} catch (error) {
		  console.error('ダッシュボード取得エラー:', error)
		}
	  })
  
	  // filteredPosts とかは既存ロジックを継承
	  const filteredPosts = computed(() => favoritePosts.value)
  
	  return {
		username,
		favoritePosts,
		filteredPosts,
		viewHistory,
		donationHistory,
		formatDateTime
	  }
	}
  }
  </script>
