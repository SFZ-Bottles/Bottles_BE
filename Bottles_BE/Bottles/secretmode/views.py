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
            'token' : token
        }
        print(token)
        return res
        
        '''
        #아이디 중복 검사
        if(Users.objects.filter(username=request.data['id']).exists()):
            return Response({ "error": "already exist id"},status=409)
        
        #이메일 중복 검사
        if(Users.objects.filter(email=request.data['email']).exists()):
            return Response({ "error": "already exist email"},status=409)

        #렝스검사
        #https://hashcode.co.kr/questions/8710/%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94-%EC%9E%A5%EA%B3%A0-is_valid%EC%9D%98-%EB%8F%99%EC%9E%91%EB%B0%A9%EC%8B%9D%EC%9D%B4-%EA%B6%81%EA%B8%88%ED%95%A9%EB%8B%88%EB%8B%A4

       
        #회원정보 저장   
        nomal_user = Users(username=request.data['id'], 
                    pw=request.data['pw'],                    
                    name = request.data['name'], 
                    email = request.data['email'], 
                    info = request.data['info']
                    )
        nomal_user.save()

        # ToDo 이메일 확인

        #secret mode account save
        random_id = RandomString.generate_random_string(10)
        maximum_iterations = 1000
        start_time = time.time()

        try:
            while not Users.objects.filter(username=random_id).exists():
                random_id = RandomString.generate_random_string(10)

                if time.time() - start_time > 10:  # 10초 이상 루프를 돌면
                    raise Exception("10초 이상 실행되어 예외를 발생시킴")

                maximum_iterations -= 1
                if maximum_iterations <= 0:
                    raise Exception("최대 반복 횟수 초과로 예외를 발생시킴")

        except Exception as e:
            # 예외를 캐치하고 처리합니다.
            print(f"예외 발생: {e}")
            return Response({"error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        secret_user = Users(username=random_id, 
                    pw=nomal_user.pw,                    
                    create_at = nomal_user.create_at
                    )
        secret_user.save()

        new_connection = Accountconnection(nomal_user = nomal_user,
                                           secret_user = secret_user,
                                           pw = nomal_user.pw)
        new_connection.save()
        '''

        # Response
        return Response({"register successfully"}, status=200)
    
