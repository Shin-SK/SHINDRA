from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from .models import Post, Category, Tag
from .serializers import PostSerializer, CategorySerializer, TagSerializer
from user.permissions import IsAdminUser, IsMemberUser, IsMemberOrPublic

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class PostListCreateView(generics.ListCreateAPIView):
    """ 投稿の一覧取得 & 作成 """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        """ `POST` は `admin` のみ許可 """
        if self.request.method == "POST":
            return [IsAdminUser()]
        return super().get_permissions()

    def get_queryset(self):
        """ ユーザーの `role` に応じて `visibility` をフィルタリング & `category` / `tag` の検索 & ソート """
        user = self.request.user
        queryset = Post.objects.exclude(visibility="unlisted")  # 🔹 `unlisted` を除外

        # 1️⃣ `role` に応じた `visibility` フィルタリング
        if not user.is_authenticated:
            queryset = queryset.filter(visibility="public")
        elif user.role == "general":
            queryset = queryset.filter(visibility="public")
        elif user.role == "member":
            queryset = queryset.filter(visibility__in=["public", "members"])

        # 2️⃣ `q`（検索ワード）で `title` & `content` をフィルタリング
        search_query = self.request.query_params.get("q")
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query)
            )  # 🔹 これで「検索ワードが含まれている投稿のみ」取得！

        # 3️⃣ `category_slug` で絞り込み（検索結果がある場合のみ適用）
        category_slug = self.request.query_params.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # 4️⃣ `tag_slug` で絞り込み（検索結果がある場合のみ適用）
        tag_slug = self.request.query_params.get("tag")
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        # 5️⃣ **🔹 検索結果を `created_at` の降順にソート**
        return queryset.order_by("-created_at")  # 新しい投稿を上に表示


class PostDetailView(generics.RetrieveAPIView):
    """ 投稿の詳細取得（slug指定）"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"

    def get_object(self):
        """ `unlisted` はログイン不要で閲覧OK、それ以外は通常の認証チェック """
        obj = super().get_object()

        # ✅ `unlisted` の場合はログイン不要でOK
        if obj.visibility == "unlisted":
            return obj

        # 🔹 `public` は誰でもOK
        if obj.visibility == "public":
            return obj

        # 🔹 `members` は `member` 以上ならOK
        user = self.request.user
        if obj.visibility == "members" and user.is_authenticated and user.role in ["member", "admin"]:
            return obj

        # 🔹 `admin` は全ての投稿を表示
        if user.is_authenticated and user.role == "admin":
            return obj

        raise NotFound("この投稿は表示できません")





