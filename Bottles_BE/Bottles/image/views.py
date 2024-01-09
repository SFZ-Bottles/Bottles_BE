from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from albums.models import Albums, Pages
from users.auth import Authenticate
from users.models import Users


import os
    

from PIL import Image
import io

class PageImageView(APIView):
    def get(self, request, id):
        resizing = request.query_params.get('resizing', False)
        width = int(request.query_params.get('width', 0))
        height = int(request.query_params.get('height', 0))

        # set image path
        if (id=='0'):
            image_path = 'MediaLibrary/ServiceImages/BottlesLogo.jpeg'
        elif id=='1':
            image_path = 'MediaLibrary/ServiceImages/BottlesLogo_locked.png'
        else:
            page_instance = Pages.objects.get(id=id)
            image_path = page_instance.item

        # check image path
        if not os.path.exists(image_path):
            return Response({"error": "Image not found"}, status=404)

        # image resizing
        if resizing:
            image = Image.open(image_path)
            if width > 0 and height > 0:
                image = image.resize((width, height), Image.Resampling.LANCZOS)#Image.ANTIALIAS)
            
            if image.mode == '1':
                # 이미지를 8비트 흑백 이미지로 변환
                image = image.convert('L')
            elif image.mode == 'CMYK':
                # 이미지를 RGB 모드로 변환
                image = image.convert('RGB')
            elif image.mode == 'YCbCr':
                # 이미지를 RGB 모드로 변환
                image = image.convert('RGB')
            elif image.mode == 'I':
                # 이미지를 8비트 흑백 이미지로 변환
                image = image.convert('L')
            elif image.mode == 'F':
                # 이미지를 8비트 흑백 이미지로 변환
                image = image.convert('L')
            elif image.mode == 'P':
                # 이미지를 RGB 모드로 변환
                image = image.convert('RGB')
                
            image_io = io.BytesIO()
            image.save(image_io, format='JPEG')
            image_data = image_io.getvalue()
        else:
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()

        response = HttpResponse(image_data, content_type='image/jpeg')
        return response
        
class AvatarImageView(APIView):
    def get(self, request, id):
        resizing = request.query_params.get('resizing', False)
        width = int(request.query_params.get('width', 0))
        height = int(request.query_params.get('height', 0))


        target_user = Users.objects.get(username=id)##################
        image_path = target_user.avatar

        # check image path
        if (not image_path) or (not os.path.exists(image_path)):
            image_path = 'MediaLibrary/ServiceImages/BottlesLogo.jpeg'

        # image resizing
        if resizing:
            image = Image.open(image_path)
            
            if width > 0 and height > 0:
                image = image.resize((width, height), Image.Resampling.LANCZOS)#Image.ANTIALIAS)
            
            if image.mode == '1':
                # 이미지를 8비트 흑백 이미지로 변환
                image = image.convert('L')
            elif image.mode == 'CMYK':
                # 이미지를 RGB 모드로 변환
                image = image.convert('RGB')
            elif image.mode == 'YCbCr':
                # 이미지를 RGB 모드로 변환
                image = image.convert('RGB')
            elif image.mode == 'I':
                # 이미지를 8비트 흑백 이미지로 변환
                image = image.convert('L')
            elif image.mode == 'F':
                # 이미지를 8비트 흑백 이미지로 변환
                image = image.convert('L')
            elif image.mode == 'P':
                # 이미지를 RGB 모드로 변환
                image = image.convert('RGB')

            image_io = io.BytesIO()
            image.save(image_io, format='JPEG')
            image_data = image_io.getvalue()
        else:
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()

        response = HttpResponse(image_data, content_type='image/jpeg')
        return response