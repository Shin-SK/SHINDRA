from django.db import models
from django.utils.text import slugify
from user.models import CustomUser

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
    slug = models.SlugField(unique=True)
    content = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', blank=True)
    image = models.ImageField(upload_to='posts/', null=True, blank=True)  # 画像フィールドを追加

    publish_at = models.DateTimeField(null=True, blank=True)
    visibility_at = models.DateTimeField(null=True, blank=True)
    member_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='draft')

    def __str__(self):
        return self.title
