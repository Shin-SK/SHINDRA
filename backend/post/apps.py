# post/apps.py
from django.apps import AppConfig

class PostConfig(AppConfig):
    name = 'post'

    def ready(self):
        import post.signals  # シグナルを読み込む