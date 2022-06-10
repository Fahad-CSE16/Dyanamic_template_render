from django.urls import path
from blogpost.post.views import BlogPostCreateView, BlogPostUpdateView, post_detail, delete_blog_post, delete_blog_comment, PostCommentCreateView

urlpatterns = [
    path('create/',BlogPostCreateView.as_view(), name="blogpost_create"),
    path('update/<int:pk>/',BlogPostUpdateView.as_view(), name="blogpost_update"),
    path('detail/<int:pk>/',post_detail, name="blogpost_detail"),
    path('delete/<int:pk>/',delete_blog_post, name="delete_blog_post"),
    path('delete_comment/<int:pk>/',delete_blog_comment, name="delete_blog_comment"),
    path('comment/create/<int:pk>/',PostCommentCreateView.as_view(), name="blog_post_comment_create"),

]
