from django.urls import path
from .views import create_user, add_audio, download_audio

urlpatterns = [
    path('user/create/', create_user),
    path('audio/add/', add_audio),
    path('record/', download_audio),
]
