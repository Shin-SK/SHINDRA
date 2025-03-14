from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model



class UserSerializer(serializers.ModelSerializer):
    user_class = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "role", "user_class"]

    def get_user_class(self, obj):
        """ `role` に応じた `user_class` を生成 """
        return obj.role  # そのまま `role` を返す

class CustomUserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        # 編集したいフィールドを含める
        fields = (
            'id', 
            'email', 
            'username',
            # 必要なら他のフィールドも
        )
        read_only_fields = ('id',)  # IDなどは編集不可にする