from django.urls import path
from albums import views

urlpatterns = [
    path('', views.FileUploadView.as_view()),
    path('<str:id>/',views.AlbumDetailView.as_view()),
]