<template>
	<div class="base-layout container-fluid">
  
	  <!-- 1) ページ先頭付近に空要素を配置し、IntersectionObserverで監視 -->
	  <div class="top-sentinel" ref="topSentinel"></div>
  
	  <!-- メインコンテンツ (router-viewなど) -->
	  <router-view />
  
	  <!-- 2) スクロールで topSentinel が画面外になったら FooterButton を表示 -->
	  <transition name="fade-slide">
		<FooterButton v-if="showFooter" />
	  </transition>
	</div>
  </template>
  
  <script>
  import { ref, onMounted, onBeforeUnmount } from 'vue'
  import FooterButton from '@/components/FooterButton.vue'
  
  export default {
	name: 'BaseLayout',
	components: {
	  FooterButton
	},
	setup() {
	  const topSentinel = ref(null)
	  const showFooter = ref(false)
	  let observer = null
  
	  onMounted(() => {
		// IntersectionObserver のコールバック
		observer = new IntersectionObserver(([entry]) => {
		  // 画面外に出た(＝スクロールした)らtrueにする
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
		if (observer) {
		  observer.disconnect()
		}
	  })
  
	  return {
		topSentinel,
		showFooter
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
  