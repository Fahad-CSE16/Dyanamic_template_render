from django.urls import path
from blogpost.api.views import BlogPostListCreateAPIView, BlogPostRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('post/',BlogPostListCreateAPIView.as_view(), name="blogpost-create-list"),
    path('post/<int:pk>/',BlogPostRetrieveUpdateDestroyAPIView.as_view(), name="blogpost-get-update-delete"),

]
