# payment/serializers.py

from rest_framework import serializers
from .models import Donation

class DonationSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source="post.title", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    # 追加: post_slug, post_image
    post_slug = serializers.CharField(source="post.slug", read_only=True)
    post_image = serializers.SerializerMethodField()

    class Meta:
        model = Donation
        fields = [
            "id", "user", "username", "post", 
            "post_title", "post_slug", "amount", "created_at",
            "post_image"
        ]

    def get_post_image(self, obj):
        """投稿画像のURLを返す。画像が無い場合は None"""
        if obj.post.image:
            request = self.context.get('request', None)
            image_url = obj.post.image.url
            # request があればフルURLに変換
            return request.build_absolute_uri(image_url) if request else image_url
        return None
