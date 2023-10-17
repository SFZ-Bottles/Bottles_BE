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

class UsernameSearchView(APIView):
    def get(self, request):
        
        target_string = self.request.query_params.get('q', '')
        num = int(self.request.query_params.get('num', 10))
        # 주어진 키워드를 포함하는 username을 갖는 사용자를 검색
        users = Users.objects.filter(username__icontains=target_string).values_list('username', flat=True)


        # 검색 결과를 리스트로 저장
        result = list(users)

        if len(result) < num:
            num = len(result)
        response_data = {
            'message': 'ok',
            'num' : num,
            'result' : result[:num]
        }

        return Response(response_data, status=status.HTTP_200_OK)
