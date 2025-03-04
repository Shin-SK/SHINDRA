from rest_framework import serializers
from .models import Post, Category, Tag

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class PostSerializer(serializers.ModelSerializer):
    category_slug = serializers.CharField(source="category.slug", read_only=True)
    tag_slugs = serializers.SerializerMethodField()
    body_class = serializers.SerializerMethodField()
    favorite_count = serializers.IntegerField(source="favorites.count", read_only=True)
    image = serializers.SerializerMethodField()  # 🔹 画像URLを追加

    class Meta:
        model = Post
        fields = ["id", "title", "slug", "content", "category", "category_slug", "tags", "tag_slugs", "body_class", "created_at", "visibility", "favorite_count", "image"]

    def get_tag_slugs(self, obj):
        return [tag.slug for tag in obj.tags.all()]  # タグのスラッグを配列で取得

    def get_body_class(self, obj):
        """
        `category_slug` + `tag_slugs` を組み合わせて `body_class` を作成
        - 英語の `slug` のみ追加
        """
        classes = [obj.category.slug] if obj.category.slug.isascii() else []  # カテゴリのslug（英語のみ）
        classes += [tag.slug for tag in obj.tags.all() if tag.slug.isascii()]  # タグのslug（英語のみ）
        return " ".join(classes)  # スペース区切りで返す

    def get_image(self, obj):
        """
        画像のURLを返す。画像がない場合は None。
        """
        if obj.image:
            request = self.context.get('request')
            image_url = obj.image.url
            return request.build_absolute_uri(image_url) if request else image_url
        return None
