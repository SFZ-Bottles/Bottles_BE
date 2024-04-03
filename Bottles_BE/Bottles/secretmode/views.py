from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import jwt, datetime, os
import time

from users.models import Users
from users.auth import Authenticate
from django.shortcuts import get_object_or_404


from secretmode.models import Accountconnection

from local_settings import JWT_SECRET_KEY


class SecretModeView(APIView):
    def post(self, request):
        user_id=Authenticate(request)
        nomal_user = Users.objects.get(id = user_id)

        if(nomal_user.pw != request.data['pw']):
            return Response({ "message": "error"},status=status.HTTP_401_UNAUTHORIZED)
        
        secret_user = Accountconnection.objects.get(nomal_user=nomal_user).secret_user

        #jwt생성
        payload = {
            'id' : secret_user.username,
            'email' : secret_user.email,
            'is_private' : secret_user.is_private,
            'exp' : datetime.datetime.now() + datetime.timedelta(days=30),
            'iat' : datetime.datetime.now()
        }

        token = jwt.encode(payload,JWT_SECRET_KEY,algorithm='HS256')
        res=Response()
        
        try:
            res.set_cookie(key= 'token', value=token, httponly= True)
        except:
            print('로그인 실패')

        res.data = {
            'token' : token,
            'id' : secret_user.username
        }
        print(token)
        return res
        
        
        #return Response({"register successfully"}, status=200)
    
