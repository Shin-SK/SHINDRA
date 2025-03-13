<template>
	<div class="home">
	  <!-- ここを監視（画面上部） -->
	  <div ref="topSentinel" class="top-sentinel"></div>
  
	  <!-- ヘッダー的なイメージ部分 -->
	  <div ref="homeWrap" class="home__wrap">
		<div class="area">
		  <div class="image">
			<img src="/logo-tate.svg" alt="">
		  </div>
		  <div class="scroll"><span></span></div>
		</div>
	  </div>
  
	  <!-- 投稿リスト。読み込み時はスピナー表示 -->
	  <div class="post-list-home">
		<div class="container-fluid">
		  <LoadingSpinner v-show="loadingPostList" />
		  <PostList v-show="!loadingPostList" />
		</div>
	  </div>
  
	  <!-- フッター -->
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
	  // フッター制御用
	  const topSentinel = ref(null)
	  const showFooter = ref(false)
	  let observer = null
  
	  // 投稿リスト読み込み中フラグ
	  const loadingPostList = ref(true)
  
	  onMounted(() => {
		// (例) ページを開いた瞬間にスクロール無効化→3秒後に解除
		document.body.style.overflow = 'hidden'
		setTimeout(() => {
		  loadingPostList.value = false
		  document.body.style.overflow = 'auto'
		}, 3000)
  
		// IntersectionObserverでtopSentinelを監視
		observer = new IntersectionObserver(([entry]) => {
		  // 画面上部(topSentinel)が見えていなければフッターを表示
		  showFooter.value = !entry.isIntersecting
		}, {
		  root: null,
		  threshold: 0
		})
  
		if (topSentinel.value) {
		  observer.observe(topSentinel.value)
		}
	  })
  
	  onBeforeUnmount(() => {
		if (observer) observer.disconnect()
	  })
  
	  return {
		topSentinel,
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
  
  /* 必要に応じて下記のようにtop-sentinelに高さを持たせることも */
  .top-sentinel {
	/* 例: 1pxの高さでも可視判定に使える */
	height: 1px;
  }
  </style>
  