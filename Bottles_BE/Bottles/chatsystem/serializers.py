from rest_framework import serializers
from .models import Chatroom, Chatparticipant, Chatmessage

class ChatroomSerializer(serializers.ModelSerializer):
    members = serializers.SerializerMethodField()

    class Meta:
        model = Chatroom
        fields = ['id', 'name', 'members', 'created_at']

    def get_members(self, obj):
        # obj는 현재 Chatroom 인스턴스입니다.
        chatparticipants = Chatparticipant.objects.filter(chatroom=obj)
        member_usernames = [chatparticipant.user.username for chatparticipant in chatparticipants]
        return member_usernames
    
class MessageSerializer(serializers.ModelSerializer):
    user_id = serializers.SerializerMethodField()
    chatroom_id = serializers.SerializerMethodField()  

    class Meta:
        model = Chatmessage
        fields = ['id', 'user_id', 'content', 'timestamp', 'chatroom_id']

    def get_user_id(self, obj):
        return obj.user.username

    def get_chatroom_id(self, obj):
        return obj.chatroom.id