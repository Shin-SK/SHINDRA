from django.urls import path
from .views import UserDetailView

urlpatterns = [
    path('', UserDetailView.as_view(), name='user-detail'),  # `''` に修正！
]
