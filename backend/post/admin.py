# post/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Post, Category, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name',)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "visibility", "image_preview", "publish_at", "member_at", "visibility_at", "created_at")
    list_filter = ("category", "tags", "visibility")
    search_fields = ("title", "content")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("title", "slug", "content", "category", "tags", "image")}),
        ("公開設定", {"fields": ("visibility", "publish_at", "member_at", "visibility_at")}),
        ("日時", {"fields": ("created_at",)}),
    )

    readonly_fields = ("created_at", "image_preview")

    def image_preview(self, obj):
        """管理画面で画像のプレビューを表示"""
        if obj.image:
            return format_html('<img src="{}" width="100" height="auto" />', obj.image.url)
        return "なし"

    image_preview.short_description = "プレビュー"
