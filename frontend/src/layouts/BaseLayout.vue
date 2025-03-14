<template>
		<!-- 1) ローディング -->
		<LoadingOverlay/>

		<div class="base-layout container-fluid">

			<div class="top-sentinel" ref="topSentinel"></div>

			<router-view />

			<div ref="bottomSentinel" style="height: 1px;"></div>

			<transition name="fade-slide">
				<FooterButton v-if="showFooter" />
			</transition>
	</div>
  </template>
  
  <script setup>
  import { ref, onMounted, onBeforeUnmount } from 'vue'
  
  const bottomSentinel = ref(null)
  const showFooter = ref(false)
  let observer = null
  
  onMounted(() => {
	observer = new IntersectionObserver(([entry]) => {
	  // "entry.isIntersecting === true" なら bottomSentinel が画面内に見えている
	  // → コンテンツが短い / またはすでに最下部にスクロール
	  if (entry.isIntersecting) {
		// ビューポート内に入った
		showFooter.value = true
	  } else {
		// ビューポート外
		showFooter.value = false
	  }
	}, {
	  root: null,
	  threshold: 0
	})
  
	if (bottomSentinel.value) {
	  observer.observe(bottomSentinel.value)
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
  