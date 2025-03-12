<template>
	<div class="posts posts--list story">
	  <!-- 投稿一覧表示 -->
	  <div class="wrap">
		<div class="contents-title">POSTS</div>
		<div class="area grid grid--list">
		  <div class="box" v-for="post in posts" :key="post.id">
			<!-- 画像リンク -->
			<router-link :to="`/posts/${post.slug}`" class="thumbnail">
			  <img v-if="post.image" v-lazy="post.image" alt="投稿画像" />
			  <img v-else src="/dummy.webp" alt="ダミー画像" />
			</router-link>
			<div class="title">
				<div class="title__wrap">
					<!-- タイトルリンク -->
					<router-link :to="`/posts/${post.slug}`">
					<h3>{{ post.title }}</h3>
					</router-link>
					<TagLinks :tags="post.tags" />
				</div>
				<!-- お気に入りボタン -->
				<FavButton :postId="post.id" :postSlug="post.slug" />
			</div>
			<!-- タグ表示 (TagLinksコンポーネントなどを使う場合) -->
			<!-- <TagLinks :tags="post.tags" /> -->
		  </div>
		</div>
	  </div>
	</div>

	<div class="search-button d-none" :class="{ visible : isScroll }">
		<button @click="toggleSearch">
			<i class="fas fa-search"></i>
		</button>
	</div>
	<section class="search" :class="{ visible : isSearchOpen }" @click="toggleSearch">
		<div class="search__wrap">
			<div class="area">
				<!-- 検索欄 -->
				<div class="text-search">
					<input
					v-model="searchTerm"
					placeholder="タイトル検索"
					@keyup.enter="applyFilters"
					/>
					<button @click="applyFilters"><i class="fas fa-search"></i>検索</button>
				</div>
			
				<!-- カテゴリ・タグのフィルタUI -->
				<div class="filter">
					<div class="wrap tag">
						<span
							v-for="tagItem in tags"
							:key="tagItem.id"
							@click="selectTag(tagItem.slug)"
							:class="{ selected: selectedTag === tagItem.slug }"
						>
							{{ tagItem.name }}
						</span>
					</div>
				</div><!-- filter -->
			</div>
		</div>
	</section>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useWindowScroll } from '@vueuse/core'
import api from '@/api'

export default {
	name: 'PostList',
	setup() {
	  const router = useRouter()
	  const route = useRoute()
  
	  // レスポンスデータ
	  const posts = ref([])
	  const categories = ref([])
	  const tags = ref([])
  
	  // フィルタ用のリアクティブ変数
	  const selectedCategory = ref('')
	  const selectedTag = ref('')
	  const searchTerm = ref('')
  
	  // --- 検索モーダルの開閉フラグ ---
	  const isSearchOpen = ref(false)

	  // --- スクロールでの表示フラグ ---
	  const isScroll = ref(false)
	  const { x, y } = useWindowScroll()

	  // 100px以上スクロールしたらボタン表示
	  watch(
		() => y.value,
		(newY) => {
		  if (newY > 100) {
			isScroll.value = true
		  } else {
			isScroll.value = false
		  }
		}
	  )

	  // ボタンクリックでモーダル表示切り替え
	  function toggleSearch() {
		isSearchOpen.value = !isSearchOpen.value
	  }

	  // --- 初期処理 ---
	  onMounted(async () => {
		try {
		  // カテゴリ一覧取得
		  const catRes = await api.get('posts/categories/')
		  categories.value = catRes.data
  
		  // タグ一覧取得
		  const tagRes = await api.get('posts/tags/')
		  tags.value = tagRes.data
  
		  // URLクエリから初期値をセット
		  if (route.query.category) {
			selectedCategory.value = route.query.category
		  }
		  if (route.query.tag) {
			selectedTag.value = route.query.tag
		  }
		  // サーバー側で ?q=... のパラメータを使っている想定
		  if (route.query.q) {
			searchTerm.value = route.query.q
		  }
  
		  // 最初の投稿一覧取得
		  await fetchPosts()
		} catch (error) {
		  console.error('API取得エラー:', error)
		}
	  })
  
	  // --- 投稿一覧をサーバーから取得 ---
	  async function fetchPosts() {
		try {
		  // クエリパラメータを用意
		  const params = {}
  
		  // カテゴリ
		  if (selectedCategory.value) {
			params.category = selectedCategory.value
		  }
		  // タグ
		  if (selectedTag.value) {
			params.tag = selectedTag.value
		  }
		  // 検索キーワード (サーバー側は `request.query_params.get("q")` で取得)
		  if (searchTerm.value) {
			params.q = searchTerm.value
		  }
  
		  // GET /api/posts/?category=...&tag=...&q=...
		  const res = await api.get('posts/', { params })
		  posts.value = res.data
		} catch (err) {
		  console.error('投稿取得エラー:', err)
		}
	  }
  
	  // --- カテゴリを選択したら ---
	  function selectCategory(slug) {
		selectedCategory.value = slug
		applyFilters()
	  }
  
	  // --- タグを選択したら ---
	  function selectTag(slug) {
		selectedTag.value = slug
		applyFilters()
	  }
  
	  // --- カテゴリ解除 ---
	  function clearCategory() {
		selectedCategory.value = ''
		applyFilters()
	  }
  
	  // --- タグ解除 ---
	  function clearTag() {
		selectedTag.value = ''
		applyFilters()
	  }
  
	  // --- フィルタを適用 (URLクエリ更新 & 再取得) ---
	  function applyFilters() {
		// クエリ作成
		const query = {}
  
		if (selectedCategory.value) {
		  query.category = selectedCategory.value
		}
		if (selectedTag.value) {
		  query.tag = selectedTag.value
		}
		if (searchTerm.value) {
		  // サーバ側が `q` で検索を受け取る
		  query.q = searchTerm.value
		}
  
		// /posts のURLクエリを更新 (Vue Router)
		router.push({
		  path: '/posts',
		  query
		})
  
		// サーバーに再リクエスト
		fetchPosts()
	  }
  
	  return {
		posts,
		categories,
		tags,
		selectedCategory,
		selectedTag,
		searchTerm,

		isSearchOpen,
		isScroll,
		toggleSearch,

		selectCategory,
		selectTag,
		clearCategory,
		clearTag,
		applyFilters
	  }
	}
}
</script>

<style scoped>
.selected {
	font-weight: bold;
	text-decoration: underline;
}
</style>
