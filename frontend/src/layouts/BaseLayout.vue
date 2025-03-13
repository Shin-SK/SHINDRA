<template>
		<!-- 1) ローディング -->
		<LoadingOverlay/>

		<div class="base-layout container-fluid">
	  <!-- 2) スクロール監視 -->
	  <div class="top-sentinel" ref="topSentinel"></div>
	  <router-view />
	  <transition name="fade-slide">
		<FooterButton v-if="showFooter" />
	  </transition>
	</div>
  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue'
  import FooterButton from '@/components/FooterButton.vue'
  import LoadingOverlay from '@/components/LoadingOverlay.vue'
  import { useLoadingStore } from '@/stores/loadingStore'
  
  // ここでPiniaのstoreを呼び出す
  const loadingStore = useLoadingStore()
  
  const topSentinel = ref(null)
  const showFooter = ref(false)
  let observer = null
  
  onMounted(() => {
	observer = new IntersectionObserver(([entry]) => {
	  // 画面外に出たらtrue
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

	.fade-enter-active,
	.fade-leave-active {
		opacity: 1;
		transition: opacity 0.3s;
	}

	.fade-enter-from,
	.fade-leave-to {
		opacity: 0;
	}
  </style>
  