from django.urls import path
from users import views

urlpatterns = [
    #users
    path('', views.UserListView.as_view()),
    path('check-duplicate-id/<str:id>/', views.CheckDuplicateIdView.as_view()),

    #auth
    path('login/', views.LoginView.as_view()),
    path('logout/', views.LogoutView.as_view()),
    path('validate-token/',views.ValidateTokenView.as_view()),
    
    #users
    path('<str:id>/',views.UserDetailView.as_view()),
    path('<str:id>/follow/',views.FollowListView.as_view()),
    path('<str:id>/follower/',views.FollowerListView.as_view()),
]


