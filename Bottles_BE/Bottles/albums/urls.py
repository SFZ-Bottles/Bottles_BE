from django.urls import path
from albums import views

urlpatterns = [
    path('', views.FileUploadView.as_view()),
    path('<str:id>/',views.AlbumDetailView.as_view()),
    #path('check-duplicate-id/<str:id>/', views.CheckDuplicateIdView.as_view()),
    #path('login/', views.LoginView.as_view()),
    #path('validate-token/',views.ValidateTokenView.as_view()),
    #path('<str:id>/',views.UserDetailView.as_view()),
    #path('user/register/', views.SignupView.as_view()),
    #path('login/', views.Broweser_LoginView.as_view()),
    #path('mobile_login/', views.NotBroweser_LoginView.as_view()),
]