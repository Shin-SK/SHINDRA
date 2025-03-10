<template>
	<div class="home">
		<div class="home__wrap">
			<div class="area">
				<div class="image">
					<img src="/logo-tate.svg" alt="">
				</div>
				<div class="scroll"><span></span></div>
			</div>
		</div>

		<div class="post-list-home">
			<PostList />
		</div>
	</div>
</template>


<script setup>
import PostList from './PostList.vue'
</script>