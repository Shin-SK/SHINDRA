<template>
	<div class="tag-links">
	  <span
		v-for="tagItem in tags"
		:key="tagItem.id"
		@click="goTag(tagItem.slug)"
		class="tag-item"
	  >
		{{ tagItem.name }}
	  </span>
	</div>
  </template>
  
  <script setup>
  import { defineProps } from 'vue'
  import { useRouter } from 'vue-router'
  
  const props = defineProps({
	tags: {
	  type: Array,
	  required: true
	}
  })
  
  const router = useRouter()
  
  function goTag(tagSlug) {
	router.push({
	  path: '/posts',
	  query: { tag: tagSlug }
	})
  }
  </script>
  