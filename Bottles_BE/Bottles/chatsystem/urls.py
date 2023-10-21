from django.urls import path
from chatsystem import views

urlpatterns = [
    path('', views.ChatRoomListView.as_view()),
    path('<str:chatroom_id>/',views.ChatRoomDetailView.as_view()),
    path('<str:chatroom_id>/messages/',views.MessagesDetailView.as_view()),
]