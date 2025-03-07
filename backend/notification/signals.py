# notifications/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from backend.post.models import Post
from .models import Notification
from backend.user.models import CustomUser  # あなたのUserモデル

@receiver(post_save, sender=Post)
def create_notification_for_new_post(sender, instance, created, **kwargs):
    if created:
        # ここで「新しい投稿が作成された時」の通知を作成する
        # 例: 全ユーザーに通知する
        users = CustomUser.objects.all()
        for user in users:
            Notification.objects.create(
                user=user,
                message=f"新しい投稿が追加されました: {instance.title}"
            )
