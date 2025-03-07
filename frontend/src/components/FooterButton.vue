<template>
	<!-- フッターボタンの大枠 -->
	<div class="footer-button"
		 :class="{
		   visible: isScroll,   // 100px以上スクロールしたらボタンが見える
		   open: isOpen         // メニュー展開中
		 }"
	>
	  <!-- オーバーレイ (メニュー開いたとき画面をクリックで閉じる) -->
	  <div class="overlay"
		   :class="{ show: isOpen }"
		   @click="toggleMenu"
	  ></div>
  
	  <!-- メインボタン (クリックでメニューを開閉) -->
	  <button class="menu-button" @click="toggleMenu">
		<img src="@/assets/image/icon.svg" alt="menu icon"
			 :class="{ rotate: isOpen }" />
	  </button>
  
	  <!-- メニュー項目 -->
	  <div class="menu" :class="{ open: isOpen }">
  
		<!-- Story -->
		<!-- <router-link :to="{ path: '/posts', query: { category: 'story' } }"
					 @click="toggleMenu">
		  <button><i class="fas fa-book"></i></button>
		</router-link> -->
  
		<!-- Podcast -->
		<!-- <router-link :to="{ path: '/posts', query: { category: 'podcast' } }"
					 @click="toggleMenu">
		  <button><i class="fas fa-podcast"></i></button>
		</router-link> -->
  
		<!-- Posts一覧 -->
		<router-link to="/posts" @click="toggleMenu">
		  <button><i class="fas fa-stream"></i></button>
		</router-link>

		<!-- ダッシュボード -->
		<router-link to="/dashboard" @click="toggleMenu">
		  <button><i class="fas fa-tachometer-alt"></i></button>
		</router-link>
  
		<!-- 設定 -->
		<router-link to="/dashboard/settings" @click="toggleMenu">
		  <button><i class="fas fa-cog"></i></button>
		</router-link>

		<!-- 
			scss button footer-buttonのボタン数を変える
		-->
  
	  </div> <!-- .menu -->
	</div> <!-- .footer-button -->
  </template>
  
<script setup>
import { ref, watch, onMounted } from 'vue'
import { useWindowScroll } from '@vueuse/core'

const isOpen = ref(false)
const isScroll = ref(false)
const { y } = useWindowScroll()

onMounted(() => {
  // コンテンツ総高さがビューポートの高さ以下なら、はじめからボタンを表示
  if (document.documentElement.scrollHeight <= window.innerHeight) {
    isScroll.value = true
  }
})

watch(
  () => y.value,
  (newY) => {
    // 100px以上スクロールしたらボタン表示
    if (newY > 100) {
      isScroll.value = true
    } else {
      isScroll.value = false
    }
  }
)

function toggleMenu() {
  isOpen.value = !isOpen.value
}
</script>
