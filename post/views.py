from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from django.db.models import Q
import re
import bleach
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

from .models import Post, Category, Tag
from .serializers import PostSerializer, CategorySerializer, TagSerializer
from user.permissions import IsAdminUser

from django_filters.rest_framework import DjangoFilterBackend
from .models import Post
from .filters import PostFilter

class PostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter
    permission_classes = [AllowAny]


class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class TagListCreateView(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


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
        """
        ユーザーの `role` に応じて `visibility` をフィルタリング & `category` / `tag` の検索 & ソート 
        """
        user = self.request.user
        print(f"DEBUG: user={user}, is_auth={user.is_authenticated}, role={getattr(user, 'role', None)}")
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
            )

        # 3️⃣ `category_slug` で絞り込み
        category_slug = self.request.query_params.get("category")
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # 4️⃣ `tag_slug` で絞り込み
        tag_slug = self.request.query_params.get("tag")
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)

        # 5️⃣ 新しい投稿を上に表示
        return queryset.order_by("-created_at")


class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"

    def get_object(self):
        """
        visibility の判定を行い:
          'unlisted' は誰でも閲覧OK
          'public'   は誰でもOK
          'members'  は会員/管理者OK
          'admin'    は管理者OK
        """
        obj = super().get_object()

        if obj.visibility == "unlisted":
            return obj
        if obj.visibility == "public":
            return obj

        user = self.request.user
        if obj.visibility == "members":
            if user.is_authenticated and user.role in ["member", "admin"]:
                return obj
            else:
                raise NotFound("この投稿は表示できません")

        if user.is_authenticated and user.role == "admin":
            return obj

        raise NotFound("この投稿は表示できません")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        # カテゴリが "Story" の場合のみカスタム変換
        if instance.category.slug == "story":
            html_content = self.custom_transform(instance.content)

            # XSS対策: bleach
            allowed_tags = ["div", "span", "br", "h1", "h2", "h3"]
            allowed_attrs = {
                "div": ["class"],
                "span": ["class"]
            }
            safe_html = bleach.clean(html_content, tags=allowed_tags, attributes=allowed_attrs, strip=True)

            # 通常のシリアライズ結果
            serializer = self.get_serializer(instance)
            data = serializer.data
            # カスタムHTMLを追加
            data["content_html"] = safe_html
            return Response(data)
        else:
            # Story以外は普通に返却
            serializer = self.get_serializer(instance)
            return Response(serializer.data)

    def custom_transform(self, text):
        """
        行ベースでHTML化:
        1) ### 数字 → 見出し行 <h3>数字</h3>
        2) 空行     → <div class="line blank"></div>
        3) "キャラ名 セリフ" → <div class="line"><div class="role">...</div><div class="speech">...</div></div>
        4) その他（ト書き） → <div class="line"><div class="role"></div><div class="speech">...</div></div>
        """
        lines = text.split("\n")
        html_lines = []

        for line in lines:
            stripped = line.strip()

            # (1) 空行
            if not stripped:
                html_lines.append('<div class="line blank"></div>')
                continue

            # (2) 見出し行 (例: ### 1 とか ### 12)
            heading_match = re.match(r'^###\s+(\d{1,2})$', stripped)
            if heading_match:
                number = heading_match.group(1)
                html_lines.append(
                    '<div class="line heading">'
                    '  <div class="role"></div>'
                    f'  <div class="speech"><h3>{number}</h3></div>'
                    '</div>'
                )
                continue

            # (3) キャラ名＋セリフ: ^(\S+)\s+(残り)
            dialogue_match = re.match(r'^(\S+)\s+(.+)', stripped)
            if dialogue_match:
                character, dialogue = dialogue_match.groups()
                html_lines.append(
                    '<div class="line">'
                    f'  <div class="role">{character}</div>'
                    f'  <div class="speech">{dialogue}</div>'
                    '</div>'
                )
            else:
                # (4) ト書き（役名なし）
                html_lines.append(
                    '<div class="line">'
                    '  <div class="role"></div>'
                    f'  <div class="speech">{stripped}</div>'
                    '</div>'
                )

        return "".join(html_lines)
