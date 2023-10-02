from rest_framework import serializers
from .models import Comments, Reply

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ('parent_comment', 'child_comment')

class ReplyDetailSerializer(serializers.ModelSerializer):
    id=serializers.CharField(source='child_comment.id')
    album_id=serializers.CharField(source='child_comment.album.id')    
    user_id=serializers.CharField(source='child_comment.made_by.username')
    mention=serializers.CharField(source='child_comment.mentioned_user.username',allow_null=True)
    comment=serializers.CharField(source='child_comment.content')
    created_at=serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ',source='child_comment.created_at') 
    updated_at=serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ',source='child_comment.updated_at')

    class Meta:
        model = Reply
        fields = ('id', 'album_id', 'user_id', 'mention','created_at','updated_at', 'comment',)


class CommentsSerializer(serializers.ModelSerializer):
    album_id=serializers.CharField(source='album.id')    
    user_id=serializers.CharField(source='made_by.username')
    mention=serializers.CharField(source='mentioned_user.username',allow_null=True)
    comment=serializers.CharField(source='content')
    reply_num=serializers.SerializerMethodField()
    #reply = ReplySerializer(many=True, read_only=True, default=[], source='reply_parent')
    reply = ReplyDetailSerializer(many=True, read_only=True, default=[], source='reply_parent')

    class Meta:
        model = Comments
        fields = ('id', 'album_id', 'user_id', 'mention','created_at','updated_at', 'comment', 'reply_num','reply')
        ordering = ['order']
    
    def get_reply_num(self, obj):
        # obj의 Reply 역참조 관계를 사용하여 Reply 쿼리셋을 가져옵니다.
        reply_queryset = obj.reply_parent.all()
        
        # Reply 쿼리셋의 길이를 반환하여 reply_num 필드로 설정합니다.
        return len(reply_queryset)

class CommentResponseSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    album_id=serializers.CharField()
    made_by = serializers.CharField(source='made_by.username')
    content = serializers.CharField()
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    updated_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    mentioned_user_id = serializers.CharField()
    parent_comment_id = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ('id', 'album_id', 'made_by', 'content', 'mentioned_user_id','created_at','updated_at', 'parent_comment_id')

    def get_parent_comment_id(self, obj):

        # child_comment 값을 가지는 객체가 존재하는지 확인
        try:
            temp_reply = Reply.objects.filter(child_comment=obj)
            parent_comments = temp_reply.values('parent_comment')
            if len(parent_comments) == 0:
                result = None
            else:
                result = parent_comments[0]['parent_comment']
            return result
        except Reply.DoesNotExist:
            return None
'''        
class CommentListResponseSerializer(serializers.ModelSerializer):
    id = serializers.CharField()
    album_id=serializers.CharField()
    user_id = serializers.CharField(source='made_by.username')
    content = serializers.CharField()
    created_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    updated_at = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')
    mention = serializers.CharField(source='mentioned_user_id')
    child_comment = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ('id', 'album_id', 'made_by', 'content', 'mentioned_user_id','created_at','updated_at', 'parent_comment_id')

    def get_parent_comment_id(self, obj):

        # child_comment 값을 가지는 객체가 존재하는지 확인
        try:
            temp_reply = Reply.objects.filter(child_comment=obj)
            parent_comments = temp_reply.values('parent_comment')
            if len(parent_comments) == 0:
                result = None
            else:
                result = parent_comments[0]['parent_comment']
            return result
        except Reply.DoesNotExist:
            return None
'''

class ReplyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ('id', 'parent_comment', 'child_comment', 'created_at')

class CommentListSerializer(serializers.ModelSerializer):
    reply = ReplyResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Comments
        fields = ('id', 'album', 'made_by', 'mentioned_user', 'created_at', 'content', 'reply')
