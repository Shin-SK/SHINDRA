<template>
	<div class="home">
	  <!-- ここを監視 -->
	  <div ref="homeWrap" class="home__wrap">
		<div class="area">
		  <div class="image">
			<img src="/logo-tate.svg" alt="">
		  </div>
		  <div class="scroll"><span></span></div>
		</div>
	  </div>
  
	  <!-- ここを"部分的"にプリローダー化したい -->
	  <div class="post-list-home">
		<div class="container-fluid">
		  <!-- 読み込み中はスピナーを表示して、PostListは隠す -->
		  <LoadingSpinner v-show="loadingPostList" />
		  <PostList v-show="!loadingPostList" />
		</div>
	  </div>
  
	  <div ref="footerSentinel"></div>
  
	  <!-- footer -->
	  <transition name="fade-slide">
		<FooterButton v-if="showFooter" />
	  </transition>
	</div>
  </template>
  
  <script>
  import { ref, onMounted, onBeforeUnmount } from 'vue'
  import PostList from './PostList.vue'
  import FooterButton from '../components/FooterButton.vue'
  import LoadingSpinner from '../components/LoadingSpinner.vue'
  
  export default {
	name: 'Index',
	components: { PostList, FooterButton, LoadingSpinner },
	setup() {
	  // Footer用
	  const footerSentinel = ref(null)
	  const showFooter = ref(false)
	  let observer = null
  
	  // PostList用 ローディング状態
	  const loadingPostList = ref(true)
  
	  onMounted(() => {
		// ① ページを表示した瞬間はスクロール無効に
      	document.body.style.overflow = 'hidden'
		// 例: 3秒後に「読み込み完了した」とみなす
		setTimeout(() => {
		  loadingPostList.value = false
		  document.body.style.overflow = 'auto'
		}, 3000)
  
		// フッター用IntersectionObserver
		observer = new IntersectionObserver(([entry]) => {
		  showFooter.value = entry.isIntersecting
		}, {
		  root: null,
		  threshold: 0
		})
  
		if (footerSentinel.value) {
		  observer.observe(footerSentinel.value)
		}
	  })
  
	  onBeforeUnmount(() => {
		if (observer) observer.disconnect()
	  })
  
	  return {
		footerSentinel,
		showFooter,
		loadingPostList
	  }
	}
  }
  </script>
  
  <style scoped>
  .fade-slide-enter-active,
  .fade-slide-leave-active {
	transition: transform 0.3s, opacity 0.3s;
  }
  .fade-slide-enter-from,
  .fade-slide-leave-to {
	transform: translateY(20px);
	opacity: 0;
  }
  </style>
  