import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

import jwt
from jwt.exceptions import InvalidSignatureError
from users.models import Users
from local_settings import JWT_SECRET_KEY

from chatsystem.models import Chatroom, Chatparticipant, Chatmessage
from django.utils import timezone

from urllib.parse import urlparse, parse_qs

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
    	# 파라미터 값으로 채팅 룸을 구별
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = 'chat_%s' % self.room_id
        self.participant = await self.get_participant()

        
        #ws://127.0.0.1:8000/ws/chat/0000006562d796995bb28f0cf6159f/
        # 인증 확인
        self.user = await self.get_user_from_scope()
        if not self.user:
            # 인증되지 않은 경우 연결 종료
            await self.close()
            return
        if not self.user in self.participant:
            # 채팅방에 권한이 없다면 연결 종료
            await self.close()
            return
        
        print(self.room_id)
        # 룸 그룹에 참가
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # 룸 그룹 나가기
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # 웹소켓으로부터 메세지 받음
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['content']
        username = text_data_json['user_id']
        created_at = timezone.now()  #text_data_json['created_at']

        result = await self.save_chat_message(username, message, created_at)

        if not result:
            await self.close()
            return

        # 룸 그룹으로 메세지 보냄
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'user_id': username,
                'content': message,
                'timestamp': created_at.isoformat(),  # ISO 포맷으로 변환
            }
        )

        

    # 룸 그룹으로부터 메세지 받음
    async def chat_message(self, event):
        message = event['content']
        username = event['user_id']
        created_at = event['timestamp']

        # 웹소켓으로 메세지 보냄
        await self.send(text_data=json.dumps({
            'user_id': username,
            'content': message,
            'timestamp': created_at,
        }))

    @database_sync_to_async
    def get_participant(self):
        try:
            # 채팅방 멤버 전달
            chatroom = Chatroom.objects.get(id=self.room_id)
            user_ids = Chatparticipant.objects.filter(chatroom=chatroom).values_list('user__id', flat=True)

            return list(user_ids)
        except Chatroom.DoesNotExist:
            # 해당하는 채팅방이 없는 경우 처리
            return []


    @database_sync_to_async
    def save_chat_message(self, username, message, created_at=None):
        try:
            # 채팅 메시지를 데이터베이스에 저장
            chatroom = Chatroom.objects.get(id=self.room_id)
            user = Users.objects.get(username=username)

            if created_at is None:
                created_at = timezone.now()

            Chatmessage.objects.create(
                chatroom=chatroom,
                user=user,
                content=message,
                timestamp=created_at,
                status=None
            )

            return True
        except Chatroom.DoesNotExist:
            # 해당하는 채팅방이 없는 경우 처리
            print("Error: Chatroom does not exist.")
            return False
        except Users.DoesNotExist:
            # 해당하는 사용자가 없는 경우 처리
            print(f"Error: User '{username}' does not exist.")
            return False
        except Exception as e:
            # 그 외의 예외 처리
            print(f"Error: {e}")
            return False

    
    @database_sync_to_async
    def get_user_from_scope(self):
        # auth 헤더에서 토큰을 추출하고 사용자를 반환하는 비동기 함수
        # URL에서 'token' 파라미터 추출
        query_params = urlparse(self.scope['query_string'].decode())
        token = parse_qs(query_params.path).get('token', [None])[0]
        #token = parse_qs(query_params.query).get('token', [None])[0]
        if token==None:
            print("토큰 없음")
            return False
        print(token)
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
            user = Users.objects.get(username = payload['id'])
            return(user.id)
        
        except jwt.ExpiredSignatureError:
            print("토큰 만료")
            return False
        
        except InvalidSignatureError:
            print("올바르지 않은 시그니처")
            return False
        
        except Users.DoesNotExist:
            print("사용자 없음")
            return False
        
        except Exception as e:
            print("기타 에러:", e)
            return False

'''
        if 'headers' in self.scope:
            headers = self.scope['headers']
            for header in headers:
                print(header)
                if header[0].decode() == 'authorization':
                    token = header[1].decode().split(' ')[1]
                
                    try:
                        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
                        user = Users.objects.get(username = payload['id'])
                        return(user.id)
                    
                    except jwt.ExpiredSignatureError:
                        print("토큰 만료")
                        return False
                    
                    except InvalidSignatureError:
                        print("올바르지 않은 시그니처")
                        return False
                    
                    except Users.DoesNotExist:
                        print("사용자 없음")
                        return False
                    
                    except Exception as e:
                        print("기타 에러:", e)
                        return False
            #return user
        else:
            return False
'''