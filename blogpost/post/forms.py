from django import forms
from blogpost.models import BlogPost, PostComment
from blogpost.forms import BaseModelForm


class BlogPostForm(BaseModelForm):
    class Meta:
        model =BlogPost
        fields = ['title', 'details']


class PostCommentForm(BaseModelForm):
    class Meta:
        model =PostComment
        fields = ['text']
