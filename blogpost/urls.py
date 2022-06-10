from django.urls import path, include
from blogpost.post import urls as post_urls

urlpatterns = [
    path('post/', include(post_urls)), 
]
