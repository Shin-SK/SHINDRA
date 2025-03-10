<template>
	<!-- フッターボタンの大枠 -->
	<div class="footer-button"
		 :class="{
		   visible: isVisible,   // 100px以上スクロールしたらボタンが見える
		   open: isOpen
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

		<router-link to="/" @click="toggleMenu">
		  <button><i class="fas fa-igloo"></i></button>
		</router-link>
  
		<!-- 設定 -->
		<router-link to="/dashboard/settings" @click="toggleMenu">
		  <button><i class="fas fa-cog"></i></button>
		</router-link>

		<a>
			<LogoutButton />
		</a>
		<!-- 
			scss button footer-buttonのボタン数を変える
		-->
  
	  </div> <!-- .menu -->
	</div> <!-- .footer-button -->
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
import LogoutButton from './LogoutButton.vue'
  
  const isOpen = ref(false)
  const isVisible = ref(false) // 初期値 false
  
  onMounted(() => {
  // 一度描画されてから次フレームでvisibleクラスをONにする
  requestAnimationFrame(() => {
    isVisible.value = true
  })
})
  
  function toggleMenu() {
	isOpen.value = !isOpen.value
  }
  </script>