import django_filters
from blogpost.models import BlogPost, PostComment


class BlogPostFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = BlogPost
        fields = ('is_active', 'created_at', 'created_by')


class PostCommentFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter()
    
    class Meta:
        model = PostComment
        fields = ('post', 'is_active', 'created_at', 'created_by')
