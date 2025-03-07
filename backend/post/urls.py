# post/urls.py
from django.urls import path
from .views import (
    PostListCreateView,
    CategoryListCreateView,
    TagListCreateView,
    PostDetailView
)

urlpatterns = [
    path('', PostListCreateView.as_view(), name='post-list-create'),
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('tags/', TagListCreateView.as_view(), name='tag-list'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail')
]
