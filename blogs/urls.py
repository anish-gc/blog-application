from django.urls import path
from .views import (
    PostListView,
    PostCreateView,
    PostDetailView,
    PostUpdateView,
    PostDeleteView,
    UserPostsView
)

urlpatterns = [
    path("posts/", PostListView.as_view(), name="post-list"),
    path('posts/my-posts/', UserPostsView.as_view(), name='user-posts'),
    path("posts/create/", PostCreateView.as_view(), name="post-create"),
    path("posts/<int:post_id>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:post_id>/update/", PostUpdateView.as_view(), name="post-update"),
    path("posts/<int:post_id>/delete/", PostDeleteView.as_view(), name="post-delete"),
]
