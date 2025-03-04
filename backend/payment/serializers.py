from rest_framework import serializers
from .models import Donation

class DonationSerializer(serializers.ModelSerializer):
    """投げ銭履歴のシリアライザー"""
    post_title = serializers.CharField(source="post.title", read_only=True)  # 投稿タイトルを追加
    username = serializers.CharField(source="user.username", read_only=True)  # ユーザー名を追加

    class Meta:
        model = Donation
        fields = ["id", "user", "username", "post", "post_title", "amount", "created_at"]
