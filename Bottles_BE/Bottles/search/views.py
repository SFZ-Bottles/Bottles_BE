from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.auth import Authenticate
from django.shortcuts import get_object_or_404

from users.models import Users
from users.serializers import UserSerializer

class UsernameSearchView(APIView):
    def get(self, request):

        user_id=Authenticate(request)
        user = get_object_or_404(Users, id=user_id)

        target_string = self.request.query_params.get('q', '')
        num = int(self.request.query_params.get('num', 10))
        # 주어진 키워드를 포함하는 username, info, avatar를 갖는 사용자를 검색
        users = Users.objects.filter(username__icontains=target_string, is_private=user.is_private)

        result = UserSerializer(users, many=True)

        if len(result.data) < num:
            num = len(result.data)
        
        response_data = {
            'message': 'ok',
            'num': num,
            'result': result.data[:num]
        }

        return Response(response_data, status=status.HTTP_200_OK)
