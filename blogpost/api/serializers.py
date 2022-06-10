from rest_framework.serializers import SerializerMethodField, ModelSerializer
from userapp.serializers import UserLiteSerializer
from blogpost.models import BlogPost, PostComment


class ReadWriteSerializerMethodField(SerializerMethodField):
    """
    Default SerializerMethodField in drf is read only.
    This method field class supports both read and write
    """

    def __init__(self, method_name=None, **kwargs):
        self.method_name = method_name
        kwargs["source"] = "*"
        self.read_only = False
        super(SerializerMethodField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        return {f'{self.field_name}_id': data}


class PostCommentLiteSerializer(ModelSerializer):
    created_by = UserLiteSerializer(read_only=True, many=False)
    class Meta:
        model = PostComment
        fields = ('id', 'text', 'is_active', 'created_at', 'created_by')


class BlogPostSerializer(ModelSerializer):
    post_comments = PostCommentLiteSerializer(source='postcomment_set', read_only=True, many=True)

    created_by = ReadWriteSerializerMethodField(required=False)
    def get_created_by(self, obj):
        if not obj.created_by:
            return None
        return UserLiteSerializer(instance=obj.created_by).data

    class Meta:
        model = BlogPost
        fields = '__all__'


class BlogPostLiteSerializer(ModelSerializer):
    created_by = UserLiteSerializer(read_only=True, many=False)

    class Meta:
        model = BlogPost
        fields = ('id', 'title', 'details', 'is_active', 'created_at', 'created_by')
        
class PostCommentSerializer(ModelSerializer):
    created_by = ReadWriteSerializerMethodField(required=False)
    post = ReadWriteSerializerMethodField()
    
    def get_created_by(self, obj):
        if not obj.created_by:
            return None
        return UserLiteSerializer(instance=obj.created_by).data

    def get_post(self, obj):
        return BlogPostLiteSerializer(obj.post, many=False).data

    class Meta:
        model = PostComment
        fields = '__all__'

    