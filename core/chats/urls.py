from django.urls import path
from .views import ChatListCreateAPIView, ChatRetrieveUpdateDestroyAPIView, MessageListCreateAPIView, MessageRetrieveUpdateDestroyAPIView


urlpatterns = [
    path('chats/', ChatListCreateAPIView.as_view(), name='chat-list'),
    path('chats/<int:pk>/', ChatRetrieveUpdateDestroyAPIView.as_view(), name='chat-detail'),
    path('messages/', MessageListCreateAPIView.as_view(), name='message-list'),
    path('messages/<int:pk>/', MessageRetrieveUpdateDestroyAPIView.as_view(), name='message-detail'),
]