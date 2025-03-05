<template>
	<div class="detail story">
		<main class="container-md" ref="pageContainer">
			<div class="detail__wrap">
				<div class="area">
					<h1>{{ post.title }}</h1>
					<div class="contents">{{ post.content }}</div>
				</div>
				<div class="thumbnail">
					<img v-if="post.image" :src="post.image" alt="投稿画像" />
				</div>

				<div class="share">
					<h2>COMMENT</h2>
					<div class="wrap">
						<i class="fab fa-twitter" @click="shareOnTwitter"></i>
					</div>
				</div>

				<div class="donate">
					<DonateButton v-if="post.id" :postId="post.id" />
				</div>
			</div>
		</main>
	</div>
</template>

<script>
import { ref, onMounted, computed } from "vue";
import { useRoute } from "vue-router";
import api from "@/api";

export default {
  setup() {
    const route = useRoute();
    const post = ref({});
    const loading = ref(true);
    const error = ref(null);

    // --- ① 閲覧履歴を追加する関数 ---
    const addToViewHistory = (postData) => {
      // 既存の履歴を取得（なければ空配列）
      let history = JSON.parse(localStorage.getItem('viewHistory') || '[]');
      // 同じIDのものがあれば一度削除（重複回避）
      history = history.filter(item => item.id !== postData.id);
      // 最新を先頭に追加
      history.unshift({
        id: postData.id,
        slug: postData.slug,
        title: postData.title,
        image: postData.image
      });
      // 件数を10件に制限
      history = history.slice(0, 10);
      // Local Storageに保存
      localStorage.setItem('viewHistory', JSON.stringify(history));
    };

    const fetchPost = async () => {
      try {
        const { slug } = route.params;
        const response = await api.get(`${import.meta.env.VITE_API_BASE_URL}posts/${slug}/`);
        post.value = response.data;

        // --- ② Postデータ取得後に履歴追加 ---
        addToViewHistory(response.data);

      } catch (err) {
        console.error("Error fetching post:", err);
        error.value = "投稿を取得できませんでした。";
      } finally {
        loading.value = false;
      }
    };

    // 記事のURLを取得
    const postUrl = computed(() => {
      return `${window.location.origin}/storys/${route.params.slug}\n`;
    });

    // Twitterでシェアする
    const shareOnTwitter = () => {
      const text = `『${post.value.title}』\n`;
      const url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(postUrl.value)}`;
      window.open(url, "_blank");
    };

    onMounted(fetchPost);

    return {
      post,
      loading,
      error,
      shareOnTwitter
    };
  },
};
</script>