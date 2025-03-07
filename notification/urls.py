# notifications/urls.py
from django.urls import path
from .views import NotificationListView, NotificationMarkAsReadView

urlpatterns = [
    path('', NotificationListView.as_view(), name='notification-list'),
    path('<int:pk>/', NotificationMarkAsReadView.as_view(), name='notification-mark'),
]
