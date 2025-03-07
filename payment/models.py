from django.db import models
from django.conf import settings
from post.models import Post

class Donation(models.Model):
    """投げ銭履歴"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    amount = models.IntegerField()  # 🔹 投げ銭の金額
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} → {self.post.title} ({self.amount}円)"
