<template>
	<div class="search-button" :class="{ visible : isScroll }">
		<button @click="toggleSearch">
			<i class="fas fa-search"></i>
		</button>
	</div>
	<section class="search" :class="{ visible : isSearchOpen }">
		<div class="search__wrap">
			<!-- 検索欄 -->
			<div class="text-search container">
				<input
				v-model="searchTerm"
				placeholder="タイトル検索"
				@keyup.enter="applyFilters"
				/>
				<button @click="applyFilters">検索</button>
			</div>
		
			<!-- カテゴリ・タグのフィルタUI -->
			<div class="filter container">
				<div class="wrap cat">
				<span
					v-for="cat in categories"
					:key="cat.id"
					@click="selectCategory(cat.slug)"
					:class="{ selected: selectedCategory === cat.slug }"
				>
					{{ cat.name }}
				</span>
				<button @click="clearCategory">全て</button>
				</div>
				<div class="wrap tag">
				<span
					v-for="tagItem in tags"
					:key="tagItem.id"
					@click="selectTag(tagItem.slug)"
					:class="{ selected: selectedTag === tagItem.slug }"
				>
					#{{ tagItem.name }}
				</span>
				<button @click="clearTag">全て</button>
				</div>
			</div><!-- filter -->
		</div>
	</section>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue'
  import { useWindowScroll } from '@vueuse/core'
  
// メニュー系

  // メニュー開閉フラグ
  const isSearchOpen = ref(false)
  
  // スクロールでの表示フラグ
  const isScroll = ref(false)
  
  // スクロール量を監視 (VueUse)
  const { x, y } = useWindowScroll()
  
  // 100px以上スクロールしたらボタン表示
  watch(
	() => y.value,
	(newY) => {
	  if (newY > 100) {
		isScroll.value = true
	  } else {
		isScroll.value = false
	  }
	}
  )
  
  // ボタンクリックでメニュー展開トグル
  function toggleSearch() {
	isSearchOpen.value = !isSearchOpen.value
  }

  // 検索系
  

  </script>
