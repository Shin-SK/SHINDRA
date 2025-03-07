from rest_framework import serializers
from .models import Favorite
from post.serializers import PostSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ["id", "post"]
