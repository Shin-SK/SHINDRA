from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),  # Django管理画面
    path('api/posts/', include('post.urls')),  # 投稿API
    path('api/users/', include('user.urls')),  # ユーザーAPI
    path('api/favorites/', include('favorite.urls')),  # 🔹 `favorite` を独立させたのでルートに追加！
    path('api/payments/', include('payment.urls')), 
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # ログイン
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # トークンリフレッシュ
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
