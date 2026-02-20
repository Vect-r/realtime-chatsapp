from django.urls import path
from .views import *

urlpatterns = [
    path('',index,name="index"),
    path("chats/",chats,name="chats"),
    path("chats/<uuid:user_id>",chats,name="userChats"),
    path("chats/<uuid:user_id>",chats,name="messageSend"),
    path("login/",login,name="login"),
    path("register/",register,name="register"),
    path("logout/",logout,name="logout")
]