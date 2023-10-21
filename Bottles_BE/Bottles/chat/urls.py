from django.urls import path
from .views import VoiceflowView

urlpatterns = [
    path('voiceflow/', VoiceflowView.as_view(), name='voiceflow'),
]
