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
    # 🔹 ここで TagSerializer を使って、タグをオブジェクト形式で返す
    tags = TagSerializer(many=True, read_only=True)

    category_slug = serializers.CharField(source="category.slug", read_only=True)
    tag_slugs = serializers.SerializerMethodField()
    body_class = serializers.SerializerMethodField()
    favorite_count = serializers.IntegerField(source="favorites.count", read_only=True)
    image = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id", "title", "slug", "content",
            "category", "category_slug",
            "tags",             # ← TagSerializerを適用したフィールド
            "tag_slugs",        # ← 既存ロジック
            "body_class", "created_at", "visibility",
            "favorite_count", "image", "is_favorited",
        ]

    def get_tag_slugs(self, obj):
        """既存のロジック通り、tag.slug の配列だけ返したい"""
        return [tag.slug for tag in obj.tags.all()]

    def get_body_class(self, obj):
        """
        `category_slug` + `tag_slugs` を組み合わせて `body_class` を作成
        - 英語の `slug` のみ追加
        """
        classes = []
        # カテゴリが英字slugなら追加
        if obj.category.slug.isascii():
            classes.append(obj.category.slug)
        # タグの slug が英字なら追加
        classes += [tag.slug for tag in obj.tags.all() if tag.slug.isascii()]

        return " ".join(classes)

    def get_image(self, obj):
        """画像のURLを返す。画像がない場合は None。"""
        if obj.image:
            request = self.context.get("request")
            image_url = obj.image.url
            return request.build_absolute_uri(image_url) if request else image_url
        return None

    def get_is_favorited(self, obj):
        """
        現在のユーザーがこの投稿をお気に入り登録しているかを返す。
        """
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            # Post モデルのインスタンスから Favorite への関連名が "favorites" なら obj.favorites
            return obj.favorites.filter(user=request.user).exists()
        return False
