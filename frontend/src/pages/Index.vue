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
  
	  <!-- ホーム画面追加バナー -->
	  <transition name="fade-slide">
		<div v-if="showA2HS" class="a2hs">
		  <div class="wrap">
			<p>
			  ホーム画面に追加して<br>
			  最新作の通知を受け取ろう
			</p>
		  </div>
		  <button @click="dismissA2HS"><i class="fas fa-times-circle"></i></button>
		</div>
	  </transition>
  
	  <!-- ページ下部に設置するダミー要素 -->
	  <div ref="bottomSentinel" class="bottom-sentinel"></div>
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
	  // ----- フッター制御 -----
	  const showFooter = ref(false)
	  const topSentinel = ref(null)
	  let topObserver = null
  
	  // ----- 投稿リスト読み込み -----
	  const loadingPostList = ref(true)
  
	  // ----- ホーム画面追加バナー -----
	  const showA2HS = ref(false)
	  const bottomSentinel = ref(null)
	  let bottomObserver = null
  
	  // 「一度閉じた/追加済みフラグ」をメモリ・localStorage 両方で管理
	  const dismissed = ref(false)
  
	  // バナー「閉じる」ボタンを押したらフラグをセット
	  function dismissA2HS() {
		dismissed.value = true
		localStorage.setItem('a2hsDismissed', 'true')
		showA2HS.value = false
	  }
  
	  onMounted(() => {
		// 例）読み込み時に一時的にスクロール無効化 → 3秒後に解除
		document.body.style.overflow = 'hidden'
		setTimeout(() => {
		  loadingPostList.value = false
		  document.body.style.overflow = 'auto'
		}, 3000)
  
		// すでにホーム画面起動(PWA)かどうか判定
		const isIOSStandalone = ('standalone' in window.navigator) && window.navigator.standalone
		const isStandaloneMedia = window.matchMedia('(display-mode: standalone)').matches
		if (isIOSStandalone || isStandaloneMedia) {
		  // すでに「ホーム画面に追加済み」なのでバナーは不要
		  localStorage.setItem('a2hsDismissed', 'true')
		}
  
		// localStorage からフラグを読み込む
		dismissed.value = localStorage.getItem('a2hsDismissed') === 'true'
  
		// もしフラグがfalse（=まだ閉じていない、追加していない）場合のみ監視
		if (!dismissed.value) {
		  bottomObserver = new IntersectionObserver(([entry]) => {
			// セッション中に「閉じる」押下で dismissed が変わったら再表示しない
			if (dismissed.value) return
			// 最下部付近に達していれば表示、離れれば非表示
			showA2HS.value = entry.isIntersecting
		  }, { threshold: 1 })
  
		  if (bottomSentinel.value) {
			bottomObserver.observe(bottomSentinel.value)
		  }
		}
  
		// フッターを表示するかどうかの監視（既存の topSentinel ロジック）
		topObserver = new IntersectionObserver(([entry]) => {
		  showFooter.value = !entry.isIntersecting
		}, { threshold: 0 })
  
		if (topSentinel.value) {
		  topObserver.observe(topSentinel.value)
		}
	  })
  
	  onBeforeUnmount(() => {
		if (topObserver) topObserver.disconnect()
		if (bottomObserver) bottomObserver.disconnect()
	  })
  
	  return {
		showFooter,
		showA2HS,
		topSentinel,
		bottomSentinel,
		loadingPostList,
		dismissA2HS,
		dismissed
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
  
  .top-sentinel,
  .bottom-sentinel {
	height: 1px; /* 一部だけでも画面内に入ればIntersectionObserverが反応 */
  }
  </style>
  