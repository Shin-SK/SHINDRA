from django.db import models
from django.conf import settings
from backend.post.models import Post

class Favorite(models.Model):
    """投稿のお気に入り機能（いいね）"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="favorites")  # 🔹 逆参照 `favorites`

    class Meta:
        unique_together = ("user", "post")  # 🔹 1ユーザー1投稿に1つの「いいね」だけ

    def __str__(self):
        return f"{self.user.username} - {self.post.title}"
