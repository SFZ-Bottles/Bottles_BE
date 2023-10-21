'''
from rest_framework import serializers
from app.models import Users

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'pw', 'name', 'email', 'info', 'create_at']

class UsersSerializer_SignUp(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'pw', 'name', 'email', 'info']
'''