from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from albums.models import Albums, Pages
from users.models import Users, Friendship
from users.auth import Authenticate

from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.core.files.uploadhandler import FileUploadHandler
from django.core.files.uploadedfile import TemporaryUploadedFile

from django.utils import timezone

from django.shortcuts import get_object_or_404

import os
import json

from albums.serializers import AlbumResponseSerializer, AlbumListSerializer

def convert_to_boolean(value):
    if value.lower() == "true" or value.lower() == "True":
        return True
    elif value.lower() == "false" or value.lower() == "False":
        return False
    elif value == True:
        return True
    elif value == False:
        return False
    else:
        raise ValueError("Invalid boolean string")

#api/albums/
@method_decorator(csrf_exempt, name='dispatch')
class FileUploadView(APIView):
    
    # get album list
    def get(self, request, *args, **kwargs):
        #아이디 및 비밀번호 확인
        #print(request.COOKIES.get('token'))
        #print(request.META.get('HTTP_AUTHORIZATION'))
        user_id=Authenticate(request)
        if(user_id==False):
            return Response({ "error": "Invalid token"},status=401)

        
        is_private = self.request.query_params.get('is_private', False)
        target = self.request.query_params.get('target', 'follow')
        counts = int(self.request.query_params.get('counts', 1))
        #num = int(self.request.query_params.get('num', 1))
        try:
             num = int(self.request.query_params.get('num', 1))
         # num은 정수로 변환되었습니다.
        except ValueError:
         # 'num'이 정수로 변환할 수 없는 문자열인 경우 예외 발생
            num = 1 # 또는 다른 기본값 설정
        order_by = self.request.query_params.get('order_by', '-created_at')

        if target == "follow":
            following_list = Friendship.objects.filter(follower=user_id).values_list('followed', flat=True)
            queryset = Albums.objects.filter(made_by_id__in=following_list, is_private=is_private).order_by(order_by)

            
        else:
            user = get_object_or_404(Users, username=target)
            #queryset = Albums.objects.filter(made_by=user, is_private=is_private).order_by(order_by)[(counts-1)*num : counts*num]
            queryset = Albums.objects.filter(made_by=user, is_private=is_private).order_by(order_by)

        serializer = AlbumListSerializer(queryset, many=True)
        totla_length=len(serializer.data)
        if (counts*num > totla_length):
            if((counts-1)*num>totla_length):
                result = []
            else :
                result =serializer.data[(counts-1)*num : totla_length]
        else:
            result =serializer.data[(counts-1)*num : counts*num]
        

        response_data = {
            "message": "ok",
            "num": len(result),
            "result": result
        }
        return Response(response_data, status=status.HTTP_200_OK)
    
    # create an album
    def post(self, request, *args, **kwargs):

        print("Request method:", request.method)
        print("Request content type:", request.content_type)
        print("Request body:", request.body)

        


        
        print("@@@@@@@@@@@@@@@@@@@@@@")
        
        print('user_id: ')
        print(request.POST.get('user_id'))
        print('num: ')
        print(request.POST.get('num'))
        print('title: ')
        print(request.POST.get('title', 'A'))
        print('preface: ')
        print(request.POST.get('preface', 'A'))
        print('data: ' )
        print(request.POST.get('data'))
        print('is_private: ')
        print(request.POST.get('is_private'))
        #get values by key
        print("@@@@@@@@@@@@@@@@@@@@@@")

        is_private = convert_to_boolean(request.POST.get('is_private'))
        num = int(request.POST.get('num'))
        user_id = request.POST.get('user_id')
        title = request.POST.get('title')
        preface = request.POST.get('preface')
        data = request.POST.get('data')

        #get user info
        user = get_object_or_404(Users, username=user_id)

        # declare album and pages
        new_album = Albums(made_by = user, 
                           is_private=is_private, 
                           title= title, 
                           preface=preface,
                           number=num)   
                        
        pages_list = []        

        if data:
            try:
                data_dict = json.loads(data)
                pages = data_dict.get('pages', [])
                for page in pages:
                    page_order = page.get('order')
                    page_species = page.get('species')
                    key = page.get('data')

                    if page_species == "text":
                        pages_data = request.POST.get(key)
                    
                    elif page_species == "image" or 'cover':
                        image_file = request.FILES.get(key)
                        # 이미지 파일 처리
                        if image_file:
                            upload_dir ='MediaLibrary/UserMedia/'+ user.id + '/images/'
                            #str(timezone.now()).replace(':', '-').replace('.', '-')
                            upload_name = user.id+ '_' + str(timezone.now()).replace(':', '-').replace('.', '-')+ '_' + image_file.name
                            if not os.path.exists(upload_dir):
                                os.makedirs(upload_dir)

                            # 이미지 파일을 서버의 디스크에 저장
                            file_path = os.path.join(upload_dir, upload_name)
                            with open(file_path, 'wb') as destination:
                                for chunk in image_file.chunks():
                                    destination.write(chunk)
                        pages_data = upload_dir + upload_name
                    
                    elif page_species == "video":
                        # 지정한 업로드 핸들러를 사용하여 파일 업로드 처리
                        with FileUploadHandler(request=request) as handler:
                            upload_name = user.username+ '_' + str(timezone.now()).replace(':', '-').replace('.', '-')+ '_' ############################ TODO
                                                                                                                            ############################ Add file name and codec
                            for chunk in handler.file:
                                if isinstance(chunk, TemporaryUploadedFile):
                                    # 동영상 파일을 저장할 디렉토리 경로 설정
                                    upload_dir = 'MediaLibrary/UserMedia/'+ user.id + '/videos/'
                                    if not os.path.exists(upload_dir):
                                        os.makedirs(upload_dir)

                                    # 파일을 서버의 디스크에 저장
                                    file_path = os.path.join(upload_dir, chunk.name)
                                    with open(file_path, 'wb') as destination:
                                        for piece in chunk.chunks():
                                            destination.write(piece)
                        pages_data = upload_dir + upload_name
                    else:
                        pass
                    
                    pages_list.append({'page_order':page_order, 'page_species':page_species, 'pages_data':pages_data})
                
                new_album.save()
                for new_page in pages_list:
                    new_page_instance = Pages( album_id = new_album.id, 
                                                    species = new_page['page_species'],
                                                    sequence = int(new_page['page_order']),
                                                    item = new_page['pages_data']
                                                    )
                    new_page_instance.save()
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON data'})
        else:
            return JsonResponse({'error': 'No data provided'})
        

        #성공
        album_serializer = AlbumResponseSerializer(new_album, context={'custom_message': 'ok'})
        return Response(album_serializer.data, status=status.HTTP_201_CREATED)
        
        #return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        
#api/albums/{id}/
@method_decorator(csrf_exempt, name='dispatch')
class AlbumDetailView(APIView):
    
    # get album detail view
    def get(self, request, id, *args, **kwargs):
        #아이디 및 비밀번호 확인
        user_id=Authenticate(request)
        if(user_id==False):
            return Response({ "error": "Invalid token"},status=401)
        
        try:
            Albums_instance = Albums.objects.get(id=id)
            album_serializer = AlbumResponseSerializer(Albums_instance, context={'custom_message': 'ok'})
        except Albums.DoesNotExist:
            return Response({ "error": "Album not found"}, status=404)
        
        return Response(album_serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, id, *args, **kwargs):
        #아이디 및 비밀번호 확인
        user_id=Authenticate(request)
        if(user_id==False):
            return Response({ "error": "Invalid token"},status=401)
        
        try:
            Albums_instance = Albums.objects.get(id=id)
            if Albums_instance.made_by.id == user_id:
                Albums_instance.delete()
                return Response({ "messege": "delete successfully"}, status=status.HTTP_200_OK)
            else :
                Response({'error': 'Unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)
            
        except Albums.DoesNotExist:
            return Response({ "error": "Album not found"}, status=404)
        
    