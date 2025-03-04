from django.urls import path
from .views import PostListCreateView, PostDetailView, CategoryListCreateView, TagListCreateView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='category-list'),
    path('tags/', TagListCreateView.as_view(), name='tag-list'),
    path('', PostListCreateView.as_view(), name='post-list'),
    path('<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
]
