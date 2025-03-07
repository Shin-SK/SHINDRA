# post/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMessage
from django.conf import settings

from .models import Post
from notification.models import Notification
from user.models import CustomUser

@receiver(post_save, sender=Post)
def notify_post_created_or_published(sender, instance, created, **kwargs):
    if created:
        # 新規投稿の場合
        if instance.visibility == "public":
            users = CustomUser.objects.all()
            message = f"公開投稿が追加されました: {instance.title}"
        elif instance.visibility == "members":
            users = CustomUser.objects.filter(role='member')
            message = f"メンバー限定投稿が追加されました: {instance.title}"
        elif instance.visibility == "draft":
            users = CustomUser.objects.filter(role='admin')
            message = f"下書き投稿が作成されました: {instance.title}"
        else:
            users = []
            message = None

        if message and users.exists():
            # 1) Notificationモデルにレコード作成
            for user in users:
                Notification.objects.create(
                    user=user,
                    message=message
                )

            # 2) メール通知を行う (BCCで一斉送信)
            recipient_emails = [u.email for u in users if u.email]
            if recipient_emails:
                subject = "新規投稿のお知らせ"
                body = (
                    f"{message}\n\n"
                    f"詳細URL: https://example.com/posts/{instance.slug}"
                )

                # 管理者アドレスを to に1件だけ入れ、実際の宛先は bcc にまとめる
                email = EmailMessage(
                    subject=subject,
                    body=body,
                    from_email=settings.DEFAULT_FROM_EMAIL,  # 例: "info@studio-shindra.com"
                    to=["info@studio-shindra.com"],           # 管理者アドレス
                    bcc=recipient_emails,                    # 全員分
                )
                email.send(fail_silently=False)

    else:
        # 既存の投稿が更新された際の処理 (予約投稿の公開時など) が必要なら書く
        pass
