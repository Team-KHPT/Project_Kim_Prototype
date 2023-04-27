from django.shortcuts import redirect
from django.urls import path

from .views import Chat, AnalyzeChat, opening_comment

urlpatterns = [
    path("", Chat.as_view()),
    path("/analyze", AnalyzeChat.as_view()),
    path("/opening", opening_comment)
]
