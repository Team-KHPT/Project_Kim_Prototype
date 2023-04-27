from django.shortcuts import redirect
from django.urls import path, include

urlpatterns = [
    path("", lambda request: redirect('/chat', permanent=True)),
    path("chat", include('chat.urls')),
]
