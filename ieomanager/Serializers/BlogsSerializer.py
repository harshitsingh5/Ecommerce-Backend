from ieomanager.models import Blogs as Blogs_model,Comments,Replies
from rest_framework import serializers,exceptions
from rest_framework.validators import UniqueValidator
from .UserSerializer import UserSerializer

class BlogsSerializer(serializers.ModelSerializer):
    heading = serializers.CharField(validators=[UniqueValidator(queryset=Blogs_model.objects.all())])
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Blogs_model
        fields = ['uuid', 'heading','slug','html_data','thumbnail','updated_at','user']
        read_only_fields = ['uuid','updated_at']
    
    def validate(self,data):
        heading = data.get('heading','')
        html_data = data.get('html_data','')
        thumbnail =data.get('thumbnail','')
        if heading and html_data and thumbnail:
            return data
        else:
            msg="Details Not provided"
            raise exceptions.ValidationError(msg)

class BlogsEditSerializer(serializers.ModelSerializer):
    heading = serializers.CharField(validators=[UniqueValidator(queryset=Blogs_model.objects.all())])
    class Meta:
        model = Blogs_model
        fields = ['uuid', 'heading','slug','html_data','thumbnail','updated_at']
        read_only_fields = ['uuid','updated_at']


class RepliesSerializer(serializers.ModelSerializer):
    reply_data = serializers.CharField()
    user = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Replies
        fields = ['uuid', 'reply_data','updated_at','user']
        read_only_fields = ['uuid','updated_at']
    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('user')
        return queryset
    
    def validate(self,data):
        return data


class CommentsSerializer(serializers.ModelSerializer):
    comment_data = serializers.CharField()
    user = UserSerializer(many=False, read_only=True)
    replies = RepliesSerializer(many=True, read_only=True)
    class Meta:
        model = Comments
        fields = ['uuid', 'comment_data','updated_at','user','replies']
        read_only_fields = ['uuid','updated_at']
    
    def validate(self,data):
        comment_data = data.get('comment_data','')
        if not comment_data:
            msg="Comment Data Not Provided"
            raise exceptions.ValidationError(msg)
        return data
