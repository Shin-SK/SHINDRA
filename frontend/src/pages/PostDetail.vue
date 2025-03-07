<template>
  <div class="detail">
    <main class="container-md">
      <div v-if="post.category_slug === 'podcast'">
        <PostPodcast :post="post" />
      </div>
      <div v-else>
        <PostDefault :post="post" />
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/api'
import PostPodcast from '@/components/PostPodcast.vue'
import PostDefault from '@/components/PostDefault.vue'

const route = useRoute()
const post = ref({})
const loading = ref(true)
const error = ref(null)

function addToViewHistory(postData) {
  let history = JSON.parse(localStorage.getItem('viewHistory') || '[]')
  history = history.filter(item => item.id !== postData.id)
  history.unshift({
    id: postData.id,
    slug: postData.slug,
    title: postData.title,
    image: postData.image
  })
  history = history.slice(0, 10)
  localStorage.setItem('viewHistory', JSON.stringify(history))
}

async function fetchPost() {
  try {
    const slug = route.params.slug
    const response = await api.get(`posts/${slug}/`)
    post.value = response.data
    addToViewHistory(response.data)
  } catch (err) {
    console.error("Error fetching post:", err)
    error.value = "投稿を取得できませんでした。"
  } finally {
    loading.value = false
  }
}

onMounted(fetchPost)

</script>
