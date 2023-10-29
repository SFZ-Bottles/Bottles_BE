from django.urls import path
from secretmode import views

urlpatterns = [
    path('auth/login/', views.SecretModeView.as_view()),
]