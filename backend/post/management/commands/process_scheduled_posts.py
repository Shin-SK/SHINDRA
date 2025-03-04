# post/management/commands/process_scheduled_posts.py
from django.core.management.base import BaseCommand
from django.utils import timezone
from post.models import Post

class Command(BaseCommand):
    help = "予約投稿を公開する"

    def handle(self, *args, **kwargs):
        now = timezone.now()

        # `member_at` を過ぎたら `draft` → `members`
        posts_to_members = Post.objects.filter(member_at__lte=now, visibility="draft")
        for post in posts_to_members:
            post.visibility = "members"
            post.save()
            self.stdout.write(self.style.SUCCESS(f"メンバー限定公開: {post.title}"))

        # `visibility_at` を過ぎたら `members` → `public`
        posts_to_public = Post.objects.filter(visibility_at__lte=now, visibility="members")
        for post in posts_to_public:
            post.visibility = "public"
            post.save()
            self.stdout.write(self.style.SUCCESS(f"一般公開: {post.title}"))

        # `publish_at` を過ぎたら `draft` → `public`（直接公開）
        posts_to_publish = Post.objects.filter(publish_at__lte=now, visibility="draft")
        for post in posts_to_publish:
            post.visibility = "public"
            post.save()
            self.stdout.write(self.style.SUCCESS(f"予約投稿: {post.title}"))
