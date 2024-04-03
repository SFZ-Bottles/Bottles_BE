from django.urls import path
from image import views

urlpatterns = [
    path('page/<str:id>/',views.PageImageView.as_view()),
    path('avatar/<str:id>/',views.AvatarImageView.as_view()),
]