from rest_framework import serializers
from users.models import Users, Friendship
from local_settings import SERVER_ADDRESS

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'pw', 'name', 'email', 'info', 'create_at']

class UsernameSerializer(serializers.ModelSerializer):
    #user_id = serializers.CharField(source='user.username')
    id = serializers.CharField(source='username')
    
    class Meta:
        model = Users
        fields = ['id']

class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(source='username')
    name = serializers.CharField()#source='name')
    email = serializers.CharField()#source='email')
    info = serializers.CharField()#source='info')
    create_at = serializers.DateTimeField()#source='create_at')
    avatar = serializers.SerializerMethodField()

    def get_avatar(self, user):
        return SERVER_ADDRESS + f'api/image/avatar/{user.username}/'
    
    class Meta:
        model = Users
        fields = ['id', 'name', 'email', 'info', 'create_at', 'avatar']







"""
class FollowListSerializer(serializers.Serializer):
    user_id = serializers.CharField(source='followed.username')

    class Meta:
        model = Friendship
        fields = ['user_id']

class FollowedListSerializer(serializers.Serializer):
    user_id = serializers.CharField(source='follower.username')

    class Meta:
        model = Friendship
        fields = ['user_id']
"""