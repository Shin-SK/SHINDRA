from rest_framework import serializers
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    user_class = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "role", "user_class"]

    def get_user_class(self, obj):
        """ `role` に応じた `user_class` を生成 """
        return obj.role  # そのまま `role` を返す
