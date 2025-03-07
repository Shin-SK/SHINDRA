from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Favorite
from backend.post.models import Post
from .serializers import FavoriteSerializer

class FavoriteListView(generics.ListAPIView):
    """ ユーザーのお気に入り投稿一覧取得 """
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

class FavoriteToggleView(APIView):
    """ 投稿のお気に入り登録・解除 """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post = Post.objects.get(id=post_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, post=post)

        if not created:
            favorite.delete()  # すでに登録されていたら削除（解除）
            return Response({"message": "お気に入り解除"}, status=status.HTTP_204_NO_CONTENT)

        return Response({"message": "お気に入り登録"}, status=status.HTTP_201_CREATED)
