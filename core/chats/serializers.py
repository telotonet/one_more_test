from rest_framework import serializers
from .models import Chat, Message
from accounts.serializers import UserSerializer
from django.contrib.auth import get_user_model


class ChatParticipantSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source='id', queryset=get_user_model().objects.all())

    class Meta:
        model = get_user_model()
        fields = ['user_id'] 


class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer()

    class Meta:
        model = Message
        fields = ['id', 'sender', 'content', 'timestamp']


class ChatSerializer(serializers.ModelSerializer):
    participants = ChatParticipantSerializer(many=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['id', 'participants', 'messages']

    def create(self, validated_data):
        members_list = validated_data.pop('participants')
        request = self.context.get('request')
        user = request.user
        chat = Chat.objects.create(**validated_data)
        chat.participants.add(user)
        
        for member_data in members_list:
            member = member_data['id']
            chat.participants.add(member)
        
        return chat


