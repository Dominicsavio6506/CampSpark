# C:\Users\acer\Desktop\CampSpark\campspark\ai_assistant\urls.py

from django.urls import path
from . import views
from .views import voice_command_api

urlpatterns = [

    # MAIN AI PAGE
    path("", views.ai_page, name="ai_page"),

    # TEXT AI (MAIN)
    path("chat/", views.ai_chat_api, name="ai_chat_api"),

]