from django.urls import path
from search import views

urlpatterns = [
    path('user/', views.UsernameSearchView.as_view()),
]