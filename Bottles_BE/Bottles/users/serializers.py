from rest_framework import serializers
from users.models import Users, Friendship

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username', 'pw', 'name', 'email', 'info', 'create_at']


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
