from django.urls import path
from .views import FavoriteListView, FavoriteToggleView

urlpatterns = [
    path("", FavoriteListView.as_view(), name="favorite-list"),
    path("<int:post_id>/", FavoriteToggleView.as_view(), name="favorite-toggle"),
]
