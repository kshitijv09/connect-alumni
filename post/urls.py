from django.urls import path
from .views import (
    PostListView,          # For listing posts
    PostCreateView,        # For creating a post
    PostDetailView,        # For retrieving/updating a post
    PostDeleteView,        # For deleting a post
    CommentListCreateView  # For listing/creating comments
)

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),  # For listing posts
    path('create/', PostCreateView.as_view(), name='post-create'),  # For creating a post
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),  # For retrieving/updating a post
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),  # For deleting a post
    path('<int:post_pk>/comments/', CommentListCreateView.as_view(), name='post-comments'),  # For listing/creating comments
] 