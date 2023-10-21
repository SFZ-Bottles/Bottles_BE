from django.urls import path
from comments import views

urlpatterns = [
    path('', views.CommentsListView.as_view()),
    path('<str:comment_id>/',views.CommentsDetatilView.as_view()),
]