<template>
	<!-- overlayVisible が true のときだけDOMを生成 -->
	<div 
	  v-if="overlayVisible" 
	  class="loading-overlay" 
	  :class="{'fade-out': fadeOutActive}"
	  @transitionend="handleTransitionEnd"
	>
	  <div class="spinner">
		<img src="/icon-wh.svg" alt="">
	  </div>
	</div>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue'
  import { useLoadingStore } from '@/stores/loadingStore'
  
  const loadingStore = useLoadingStore()
  
  // オーバーレイが表示されているかどうか
  const overlayVisible = ref(false)
  // フェードアウト中かどうか
  const fadeOutActive = ref(false)
  
  // isLoading が変わるのを監視
  watch(
	() => loadingStore.isLoading,
	(newVal) => {
	  if (newVal) {
		// ローディング開始時
		fadeOutActive.value = false      // フェードアウト状態を解除
		overlayVisible.value = true      // DOMを生成（表示する）
	  } else {
		// ローディング終了時 → フェードアウト開始
		fadeOutActive.value = true
	  }
	}
  )
  
  // フェードアウトが終わったらDOMを消す
  function handleTransitionEnd() {
	// fadeOutActive が true なら、フェードアウト完了した合図
	if (fadeOutActive.value) {
	  overlayVisible.value = false
	}
  }
  </script>
