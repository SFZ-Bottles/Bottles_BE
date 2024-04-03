from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from users.auth import Authenticate
from local_settings import JWT_SECRET_KEY

from django.shortcuts import get_object_or_404

from .models import Chatroom, Chatparticipant, Chatmessage
from .serializers import ChatroomSerializer, MessageSerializer

from users.models import Users
from django.db.models import Count

#api/chatrooms/
class ChatRoomListView(APIView):
    #채팅방 생성
    def post(self, request):
        
        #변수 세팅
        data = request.data
        members = data.get('members', [])

        # 채팅방 중복 체크
        existing_chatrooms = (
            Chatroom.objects
            .filter(chatparticipant__user__username__in=members)
            .values('id')
            .annotate(member_count=Count('chatparticipant__user'))
            .filter(member_count=len(members))
        )

        # 모든 참여자가 해당 채팅방에 참여 중인지 확인
        for chatroom_data in existing_chatrooms:
            chatroom_id = chatroom_data['id']

            # 해당 채팅방에 속한 모든 참여자
            participants_in_chatroom = Chatparticipant.objects.filter(chatroom_id=chatroom_id)

            # 모든 members가 해당 채팅방에 참여 중인지 확인
            is_all_members_participating = all(participant.user.username in members for participant in participants_in_chatroom)

            if is_all_members_participating:
                # 이미 존재하는 채팅방의 경우
                return Response({'error': 'Already existing chatroom.'}, status=status.HTTP_409_CONFLICT)

        
        #chat room 생성
        chatroom = Chatroom(name=data['name']) #ToDo: 없을 경우 에러핸들링 필요
        chatroom.save()

        #멤버배정
        for i in range(0,len(members)):
            #get user info  
            member = get_object_or_404(Users, username=members[i])
            #create partipants instance
            participants = Chatparticipant(user = member,
                                           chatroom = chatroom)
            participants.save()

        #seriarizer생성 
        serializer = ChatroomSerializer(chatroom)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        target = request.GET.get('target')
        num = request.GET.get('num', '0')

        member = get_object_or_404(Users, username=target)
        chatparticipants = Chatparticipant.objects.filter(user=member)
        chatroom_ids = chatparticipants.values_list('chatroom', flat=True)
        if num == '0' or num is None:
            chatrooms = Chatroom.objects.filter(id__in=chatroom_ids)
        else:
            chatrooms = Chatroom.objects.filter(id__in=chatroom_ids).order_by('-created_at')[:int(num)]

        serializer = ChatroomSerializer(chatrooms, many=True)

        data = {
            "message": "ok",
            "num": len(chatrooms),
            "result": serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)

#api/chatrooms/{chatroom_id}}/
class ChatRoomDetailView(APIView):
    def get(self, request, chatroom_id):
        try:
            target_chatroom = Chatroom.objects.get(id=chatroom_id)  # Chatroom 대문자를 사용합니다.
        except Chatroom.DoesNotExist:
            return Response({"detail": "Chatroom not found"}, status=status.HTTP_404_NOT_FOUND)
        result=ChatroomSerializer(target_chatroom)
        
        return Response(result.data, status=status.HTTP_200_OK)

#api/messages/{chatroom_id}}/messages/
class MessagesDetailView(APIView):
    def post(self, request, chatroom_id):
        # MessageSerializer를 사용하여 데이터 유효성 검사
        serializer = MessageSerializer(data=request.data)

        if serializer.is_valid():
            # 유효한 데이터에서 user_id를 사용하여 User 모델에서 사용자를 가져옴
            user_id = request.data['user_id']
            user = Users.objects.get(username=user_id)  # ToDo: 예외 처리

            chatroom = Chatroom.objects.get(id=chatroom_id)  # ToDo: 예외 처리

            # Chatmessage 모델에 새로운 레코드 생성
            new_message = Chatmessage(
                user=user,
                chatroom_id=chatroom_id,
                content=request.data['content']
            )
            new_message.save()  # 저장

            result = MessageSerializer(new_message)

            return Response(result.data, status=status.HTTP_200_OK)

            
        else:
            errors = serializer.errors
            return Response({"error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def get(self, request, chatroom_id):
        order = request.GET.get('order', '-timestamp')
        num = int(request.GET.get('num', '30'))
        count = int(request.GET.get('count', '1'))

        chatroom = get_object_or_404(Chatroom, id=chatroom_id)
        
        messages = Chatmessage.objects.filter(chatroom=chatroom).order_by(order)
        
        # index 설정
        total_num = messages.count()
        first_index = num*(count-1)
        last_index = first_index+num-1
        
        if( (total_num-1) < first_index):
            result_messages = []
        else:
            last_index = min(total_num, last_index)
            result_messages = messages[first_index:last_index+1]
        
        serializer = MessageSerializer(result_messages, many=True)

        data = {
            "message": "ok",
            "num": len(serializer.data),
            "result": serializer.data
        }

        return Response(data, status=status.HTTP_200_OK)