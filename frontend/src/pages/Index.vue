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
  
	  <div class="post-list-home">
		<div class="container-fluid">
		<PostList />
		</div>
	  </div>
  
		<transition name="fade-slide">
			<FooterButton v-if="showFooter" />
		</transition>
	</div>
  </template>
  
  <script>
  import { ref, onMounted, onBeforeUnmount } from 'vue'
  import PostList from './PostList.vue'
  import FooterButton from '../components/FooterButton.vue'
  
  export default {
	name: 'Index',
	components: { PostList, FooterButton },
	setup() {
	  const homeWrap = ref(null)
	  const showFooter = ref(false)
	  let observer = null
  
	  onMounted(() => {
		// Intersection Observer
		observer = new IntersectionObserver((entries) => {
		  const entry = entries[0]
		  // 交差している割合: entry.intersectionRatio (0～1)
		  // 0 なら完全に画面外、1 なら完全に画面内
		  if (entry.intersectionRatio <= 0) {
			// home__wrap が完全に消えたら
			showFooter.value = true
		  } else {
			// まだ画面内に少しでも残っていれば
			showFooter.value = false
		  }
		}, {
		  root: null,        // ビューポート基準
		  threshold: 0.0     // 0% (完全に外れたら false)
		})
  
		if (homeWrap.value) {
		  observer.observe(homeWrap.value)
		}
	  })
  
	  onBeforeUnmount(() => {
		if (observer) {
		  observer.disconnect()
		}
	  })
  
	  return {
		homeWrap,
		showFooter
	  }
	}
  }
  </script>
  

  <style scoped>
.fade-slide-enter-active, .fade-slide-leave-active {
  transition: transform 0.3s, opacity 0.3s;
}
.fade-slide-enter-from, .fade-slide-leave-to {
  transform: translateY(20px);
  opacity: 0;
}
</style>