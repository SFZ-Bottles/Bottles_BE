from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import jwt, datetime, os
import time

from users.models import Users, Friendship
from users.serializers import UsersSerializer, UsernameSerializer
from users.auth import Authenticate
from local_settings import JWT_SECRET_KEY, SERVER_ADDRESS

from django.shortcuts import get_object_or_404

from django.utils import timezone

from users.utils.randomString_utils import RandomString

from secretmode.models import Accountconnection

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
            while Users.objects.filter(username=random_id).exists():
                print(f'target: {Users.objects.filter(username=random_id).exists()}')
                print(f'id: {random_id}')
                random_id = RandomString.generate_random_string(10)

                if time.time() - start_time > 10:  # 10초 이상 루프를 돌면
                    nomal_user.delete()
                    raise Exception("10초 이상 실행되어 예외를 발생시킴")

                maximum_iterations -= 1
                if maximum_iterations <= 0:
                    nomal_user.delete()
                    raise Exception("최대 반복 횟수 초과로 예외를 발생시킴")

        except Exception as e:
            # 예외를 캐치하고 처리합니다.
            nomal_user.delete()
            print(f"예외 발생: {e}")
            return Response({"error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        print(11111)
        secret_user = Users(username=random_id, 
                    pw=nomal_user.pw,                    
                    create_at = nomal_user.create_at,
                    is_private = True
                    )
        secret_user.save()
        print(22222)

        new_connection = Accountconnection(nomal_user = nomal_user,
                                           secret_user = secret_user,
                                           pw = nomal_user.pw)
        new_connection.save()
        print(33333)

        # Response
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
            'is_private' : user.is_private,
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
    
#api/auth/validate-token/
class ValidateTokenView(APIView):
    def post(self, request):
        #아이디 및 비밀번호 확인
        id=Authenticate(request)
        if(id==False):
            return Response({ "error": "Invalid token"},status=401)
        else:
            return Response({ "message": "valid token"},status=200)

#api/users/{user_id}/follow/
class FollowListView(APIView):
    
    #팔로우 요청
    def post(self, request, id):

        """
        #Authenticate
        #아이디 및 비밀번호 확인
        user_id=Authenticate(request)
        if(user_id==False):
            return Response({ "error": "Invalid token"},status=401)
        """

        #variable declare
        follower_id = id
        followed_id = request.data['target_user_id']
        follower = Users.objects.get(username=follower_id)
        followed = Users.objects.get(username=followed_id)

        #matching
        friendship_instance = Friendship(follower=follower, followed=followed)
        friendship_instance.save()

        #response
        return Response({ "message": "ok, " + follower_id + " is now following user with ID "+ followed_id}
                        ,status=status.HTTP_201_CREATED)        
        
    
    #팔로잉 리스트 요청
    def get(self, request, id):
        """
        #Authenticate
        #아이디 및 비밀번호 확인
        user_id=Authenticate(request)
        if(user_id==False):
            return Response({ "error": "Invalid token"},status=401)
        """
        user = get_object_or_404(Users, username=id)
        following_list = Friendship.objects.filter(follower=user.id).order_by('-created_at').values_list('followed', flat=True)
        queryset = Users.objects.filter(id__in=following_list)

        serializer = UsernameSerializer(queryset, many=True)

        response_data = {
            "message": "ok",
            "num": len(serializer.data),
            "result": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


#api/users/{user_id}/follower/
class FollowerListView(APIView):
    
    #팔로워 리스트 요청
    def get(self, request, id):
        """
        #Authenticate
        #아이디 및 비밀번호 확인
        user_id=Authenticate(request)
        if(user_id==False):
            return Response({ "error": "Invalid token"},status=401)
        """
        user = get_object_or_404(Users, username=id)
        following_list = Friendship.objects.filter(followed=user.id).order_by('-created_at').values_list('follower', flat=True)
        queryset = Users.objects.filter(id__in=following_list)

        serializer = UsernameSerializer(queryset, many=True)

        response_data = {
            "message": "ok",
            "num": len(serializer.data),
            "result": serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


from django.core.files.uploadedfile import InMemoryUploadedFile

#api/auth/validate-token/
class UserDetailView(APIView):
    def get(self, request, id):
        user = Users.objects.get(username=id) # id랑 같은 값을 갖는 데이터 탐색 (남들이 보기에 id == 백엔드의 username)
        return Response({
            "id": user.username,           	
            "name": user.name,       
            "email": user.email,  
            "info": user.info, 
            "created_at" : user.create_at,
            "avatar" : SERVER_ADDRESS + 'api/image/avatar/'+ user.username +'/'

        },status=200)
    

    def put(self, request, id):
        user = Users.objects.get(username=id)
 
        # 각 필드에 대한 업데이트를 수행
        for key, value in request.data.items():
            if key == 'avatar' and isinstance(value, InMemoryUploadedFile):

                ##############################################################################기존이미지 삭제
                unique_filename = user.id+ '_' + str(timezone.now()).replace(':', '-').replace('.', '-')+ '_' + value.name
                avatar_path ='MediaLibrary/UserProfile/'+ user.id + '/image/' 
                
                # 디렉토리가 존재하지 않으면 생성
                if not os.path.exists(avatar_path):
                    os.makedirs(avatar_path)
                
                with open(avatar_path+ unique_filename, 'wb') as file:
                    for chunk in value.chunks():
                        file.write(chunk)
                
                user.avatar = avatar_path+unique_filename
            
            elif key == 'id':
                setattr(user, 'username', value)
                
            else:
                setattr(user, key, value)

        user.save()
        
        return Response("User updated successfully", status=status.HTTP_200_OK)  

    #유저정보 삭제
    def delete(self, request, id):
        try:
            nomal_user = Users.objects.get(username=id)
            if(nomal_user.pw == request.data['pw']):
                accountconnection_instance = Accountconnection.objects.get(nomal_user = nomal_user)
                secret_user = accountconnection_instance.secret_user
                secret_user.delete()                
                nomal_user.delete()
                return HttpResponse("User deleted successfully", status=200)
            else:
                return HttpResponse("Wrong pw", status=401)    
        except Users.DoesNotExist:
            return HttpResponse("User not found", status=404)