from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.auth import Authenticate
from django.shortcuts import get_object_or_404

from .models import Comments, Reply
from users.models import Users
from albums.models import Albums

from .serializers import CommentsSerializer, CommentResponseSerializer, CommentDetailSerializer

class CommentsListView(APIView):
    def get(self, request):
        album_id = request.query_params.get('album_id')
        if album_id is None:
            return Response({'message': 'Missing album_id parameter'}, status=status.HTTP_400_BAD_REQUEST)

        # Comments 모델에서 album_id에 해당하는 댓글들을 가져오는 로직을 구현해야 합니다.
        # reply 모델의 child_comment 필드에 연결되지 않는 댓글들을 가져옵니다.
        comments = Comments.objects.filter(album_id=album_id).exclude(reply_child__isnull=False)

        # CommentSerializer를 사용하여 데이터를 직렬화합니다.
        serializer = CommentsSerializer(comments, many=True)

        # Reply 수를 계산하여 'reply_num' 필드 추가
        #for comment_data in serializer.data:
        #    comment_data['reply_num'] = len(comment_data['reply'])

        response_data = {
            'message': 'ok',
            'num': len(serializer.data),
            'result': serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            album_id = request.data['album_id']
            made_by_username = request.data['made_by']
            content = request.data['content']
            mentioned_user_id = request.data.get('mentioned_user_id') #request.data['mentioned_user_id']
            parent_comment_id = request.data.get('parent_comment_id') #request.data['parent_comment_id']

            target_album=get_object_or_404(Albums, id=album_id)
            owner =get_object_or_404(Users, username=made_by_username)

            # 필요한 데이터를 가지고 있는지 확인하고 누락된 경우 400 Bad Request 반환
            if not album_id or not made_by_username:
                return Response({'error': 'Missing required data'}, status=status.HTTP_400_BAD_REQUEST)  

            # Comments 모델에 데이터 저장
            if not mentioned_user_id:
                new_comment = Comments(album_id =  album_id,
                                    made_by = owner,
                                    content = content)
            else:
                mentioned_user=get_object_or_404(Users, username=mentioned_user_id)
                new_comment = Comments(album_id =  album_id,
                                    made_by = owner,
                                    content = content,
                                    mentioned_user =mentioned_user)

            new_comment.save()
            # parent가 있는 경우
            if parent_comment_id is not None and parent_comment_id != 'null':
                new_reply = Reply(parent_comment_id= parent_comment_id, child_comment_id= new_comment.id)
                new_reply.save()
            
            #응답
            result = Comments.objects.get(id=new_comment.id)
            serializer = CommentResponseSerializer(result)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CommentsDetatilView(APIView):
    def get(self, request, comment_id):
        comments = Comments.objects.filter(id=comment_id) #.exclude(reply_child__isnull=False)

        # CommentSerializer를 사용하여 데이터를 직렬화합니다.
        serializer = CommentDetailSerializer(comments)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, comment_id):
        comments = Comments.objects.get(id=comment_id) #.exclude(reply_child__isnull=False)
        comments.content = request.data['content']
        comments.save()
        # CommentSerializer를 사용하여 데이터를 직렬화합니다.
        serializer = CommentDetailSerializer(comments)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, comment_id):
        user_id=Authenticate(request)
        if(user_id==False):
            return Response({ "error": "Invalid token"},status=401)
        comments = Comments.objects.get(id=comment_id)
        if (user_id== comments.made_by.id):
            comments.delete()
            return Response({'message':'ok'}, status=status.HTTP_200_OK)
        else:
            return Response({'error':'Unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)
        
    
