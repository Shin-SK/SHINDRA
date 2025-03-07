# notifications/views.py
from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListView(generics.ListAPIView):
    """
    GET /api/notifications/
    で現在ログイン中のユーザの未読通知一覧を返す例
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user,
            is_read=False
        ).order_by('-created_at')

class NotificationMarkAsReadView(generics.UpdateAPIView):
    """
    PATCH /api/notifications/<pk>/
    で is_read=True にする処理など
    """
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        # 例: その通知が自分のものだけに制限
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionError("Cannot mark others' notifications as read.")
        serializer.save(is_read=True)
