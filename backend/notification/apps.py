# notification/apps.py
from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    name = 'notification'

    def ready(self):
        import notification.signals  # シグナルを読み込む
