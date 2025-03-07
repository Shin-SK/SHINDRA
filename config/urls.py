from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import MyConfirmEmailView
# from post.views import PostListCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path("api/posts/", PostListCreateView.as_view(), name="post-list-create"),
    path('api/posts/', include('post.urls')),
    path('api/users/', include('user.urls')),
    path('api/favorites/', include('favorite.urls')),
    path('api/payments/', include('payment.urls')),
    path('api/notifications/', include('notification.urls')),
    path('api/dj-rest-auth/', include('dj_rest_auth.urls')),
    path(
      'api/dj-rest-auth/registration/account-confirm-email/<str:key>/',
      MyConfirmEmailView.as_view(),
      name='account_confirm_email'
    ),
    path(
      'api/dj-rest-auth/registration/',
      include('dj_rest_auth.registration.urls')
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
