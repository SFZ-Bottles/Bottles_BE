from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import jwt, datetime

from users.models import Users
from users.serializers import UsersSerializer
from users.auth import Authenticate
from local_settings import JWT_SECRET_KEY


#api/users/
class UserListView(APIView):
    def post(self, request):
        #아이디 중복 검사
        if(Users.objects.filter(username=request.data['id']).exists()):
            return Response({ "error": "already exist id"},status=409)
        
        #이메일 중복 검사
        if(Users.objects.filter(email=request.data['email']).exists()):
            return Response({ "error": "already exist email"},status=409)

        #렝스검사
        #https://hashcode.co.kr/questions/8710/%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94-%EC%9E%A5%EA%B3%A0-is_valid%EC%9D%98-%EB%8F%99%EC%9E%91%EB%B0%A9%EC%8B%9D%EC%9D%B4-%EA%B6%81%EA%B8%88%ED%95%A9%EB%8B%88%EB%8B%A4

        #회원정보저장
        
        #data = JSONParser().parse(request)
        
        '''
        serializer = UsersSerializer_SignUp(data=request.data)  
        if serializer.is_valid():
            serializer.save()
            return Response({"register successfully"},status=200)
        
        #need to fix
        else:
            return Response({"error..."},status=500)
        '''
       
        #회원정보 저장   

        user = Users(username=request.data['id'], 
                    pw=request.data['pw'],                    
                    name = request.data['name'], 
                    email = request.data['email'], 
                    info = request.data['info']
                    )
        user.save()
        return Response({"register successfully"}, status=200)
    
    def get(self, request):
        all_users = Users.objects.all()
        serializer = UsersSerializer(all_users, many=True)
        return JsonResponse(serializer.data, safe=False)
    
#api/users/check-duplicate-id/{id}/
class CheckDuplicateIdView(APIView):
    def post(self, request, id):
         # 아이디 중복 검사
        if Users.objects.filter(username=id).exists():
            return Response({"error": "already exist id"}, status=status.HTTP_409_CONFLICT)
        else:
            # 중복되지 않은 경우에 대한 로직 처리
            return Response({"message": "ok, available id"}, status=status.HTTP_200_OK)
    def get(self, request, id):
         # 아이디 중복 검사
        if Users.objects.filter(username=id).exists():
            return Response({"error": "already exist id"}, status=status.HTTP_409_CONFLICT)
        else:
            # 중복되지 않은 경우에 대한 로직 처리
            return Response({"message": "ok, available id"}, status=status.HTTP_200_OK)
        

#api/auth/login/
class LoginView(APIView):
    def post(self, request):
        #아이디 및 비밀번호 확인
        try:
            user = Users.objects.get(username=request.data['id'])
            if(user.pw != request.data['pw']):
                return Response({ "error": "wrong password"},status=401)
        except Users.DoesNotExist:
            return Response({ "error": "Invalid id"},status=401)
        except Users.MultipleObjectsReturned:
            return Response({ "fatal error": "interserver error.(duplicated id)"},status=500)
        #jwt생성
        payload = {
            'id' : user.username,
            'email' : user.email,
            'exp' : datetime.datetime.now() + datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.now()
        }

        token = jwt.encode(payload,JWT_SECRET_KEY,algorithm='HS256')
        res=Response()
        
        try:
            res.set_cookie(key= 'token', value=token, httponly= True)
        except:
            pass

        res.data = {
            'token' : token
        }
        return res
    
#api/auth/validate-token/
class ValidateTokenView(APIView):
    def post(self, request):
        #아이디 및 비밀번호 확인
        id=Authenticate(request)
        if(id==False):
            return Response({ "error": "Invalid token"},status=401)
        else:
            return Response({ "message": "valid token"},status=200)


#api/auth/validate-token/
class UserDetailView(APIView):
    def get(self, request, id):
        user = Users.objects.get(username=id) # id랑 같은 값을 갖는 데이터 탐색 (남들이 보기에 id == 백엔드의 username)
        return Response({
            "id": user.username,           	
            "name": user.name,       
            "email": user.email,  
            "info": user.info 

        },status=200)
    
    #유저 정보 수정
    def put(self, request, id):
        user = Users.objects.get(username=id) # id랑 같은 값을 갖는 데이터 탐색 (남들이 보기에 id == 백엔드의 username)
        pass # 일하세요 동은씨
    
    #유저정보 삭제
    def delete(self, request, id):
        user = Users.objects.get(username=id) # id랑 같은 값을 갖는 데이터 탐색 (남들이 보기에 id == 백엔드의 username)
        pass # 일하세요 동은씨