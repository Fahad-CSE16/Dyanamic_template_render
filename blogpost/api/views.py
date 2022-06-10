from django.utils.decorators import method_decorator
import logging
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from blogpost.models import BlogPost, PostComment
from blogpost.api.serializers import BlogPostLiteSerializer, BlogPostSerializer
from blogpost.filters import BlogPostFilter
from blogpost.decorators import exception_handler
from blogpost.permissions import IsOwner
logger = logging.getLogger('django_log')


class BlogPostListCreateAPIView(ListCreateAPIView):
    permission_classes= (IsAuthenticated, )
    queryset = BlogPost.objects.filter().select_related('created_by').prefetch_related('postcomment_set__created_by')
    serializer_class = BlogPostSerializer
    search_fields = ['$title']
    filterset_class = BlogPostFilter

    @method_decorator(exception_handler)
    def create(self, request, *args, **kwargs):
        request.data['created_by'] = self.request.user.id
        logger.info('New Blog Created')
        return super(BlogPostListCreateAPIView, self).create(request, *args, **kwargs)


class BlogPostRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes =  (IsAuthenticated, IsOwner)
    queryset = BlogPost.objects.filter().select_related('created_by').prefetch_related('postcomment_set__created_by')
    serializer_class = BlogPostSerializer
    http_method_names = ['get', 'patch', 'delete']

    @method_decorator(exception_handler)
    def patch(self, request, *args, **kwargs):
        return super(BlogPostRetrieveUpdateDestroyAPIView, self).patch(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({"message":"Successfully Deleted!"}, status=status.HTTP_200_OK)
