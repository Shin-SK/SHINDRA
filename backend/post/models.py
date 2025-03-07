import uuid
from django.db import models
from django.utils.text import slugify
from backend.user.models import CustomUser
from cloudinary.models import CloudinaryField

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Post(models.Model):
    VISIBILITY_CHOICES = [
        ("draft", "下書き"),
        ("members", "メンバー限定"),
        ("public", "全員公開"),
        ("unlisted", "限定公開（URLでのみ閲覧可能）"),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)  # ← ここで blank=True を追加
    content = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True)
    # image = models.ImageField(upload_to='posts/', null=True, blank=True)
    image = CloudinaryField('image', blank=True, null=True)
    publish_at = models.DateTimeField(null=True, blank=True)
    visibility_at = models.DateTimeField(null=True, blank=True)
    member_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='draft')

    def save(self, *args, **kwargs):
        if not self.slug:
            # slug が未設定なら、短いuuidを生成
            self.slug = uuid.uuid4().hex[:8]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


from django.db import models

class YouTubeVideo(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()

    def embed_url(self):
        """YouTubeのURLを埋め込みURLに変換"""
        if "youtube.com/watch?v=" in self.url:
            video_id = self.url.split("v=")[1].split("&")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        elif "youtu.be/" in self.url:
            video_id = self.url.split("youtu.be/")[1].split("?")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return None
