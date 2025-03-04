<template>
	<div class="footer-button" :class="{ open: isOpen }">
	  <div class="overlay" :class="{ show: isOpen }" @click="toggleMenu"></div>
  
	  <button class="menu-button" @click="toggleMenu">
		<img :src="iconPath" alt="menu icon" :class="{ rotate: isOpen }">
	  </button>
  
	  <div class="menu" :class="{ open: isOpen }">
		<router-link :to="{ path: '/posts', query: { category: 'story' } }" @click="toggleMenu">
			<button><i class="fas fa-book"></i></button>
		</router-link>
		<router-link :to="{ path: '/posts', query: { category: 'podcast' } }" @click="toggleMenu">
			<button><i class="fas fa-podcast"></i></button>
		</router-link>
		<router-link to="/mypage" @click="toggleMenu">
			<button><i class="fas fa-tachometer-alt"></i></button>
		</router-link>
	  </div>
	</div>
</template>

<script>
export default {
	data() {
	  return {
		isOpen: false,
		iconPath: new URL('@/assets/image/icon.svg', import.meta.url).href, // Vue での画像パス
	  };
	},
	methods: {
	  toggleMenu() {
		this.isOpen = !this.isOpen;
	  },
	  action(icon) {
		alert(`Clicked: ${icon}`);
		this.isOpen = false;
	  }
	}
};
</script>
