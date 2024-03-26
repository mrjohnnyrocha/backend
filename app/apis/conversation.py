import uuid
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from app.apis.base import BaseAPI

from app.models import Conversation, Message, CustomUser
from app.serializers import ConversationSerializer, MessageSerializer

class ConversationAPI(BaseAPI):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def __init__(self):
        super().__init__()

    def get(self, request, name=None, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'User must be authenticated.'}, status=status.HTTP_403_FORBIDDEN)

        conversations = Conversation.objects.filter(members=request.user, name=name)
        serialized_conversations = []
        for conversation in conversations:
            messages = conversation.messages.all()
            conversation_data = ConversationSerializer(conversation).data
            conversation_data['messages'] = MessageSerializer(messages, many=True).data
            serialized_conversations.append(conversation_data)

        return Response(serialized_conversations, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        print(request.data) # Debugging
        if not request.user.is_authenticated:
            return Response({'error': 'User must be authenticated.'}, status=status.HTTP_403_FORBIDDEN)

        conversation_id = request.data.get('conversation_id')
        name = request.data.get('name')
        try:
            conversation = Conversation.objects.get(name=name)
            conversation_id = conversation.uuid
        except Conversation.DoesNotExist:
            conversation_id = uuid.uuid4()
            conversation = Conversation.objects.create(uuid=conversation_id, name=name)
        message_data = request.data.get('message_data', {})

        try:
            conversation = Conversation.objects.get(uuid=conversation_id)
        except Conversation.DoesNotExist:
            conversation = Conversation.objects.create(uuid=uuid.uuid4(), name=name)

        conversation.members.add(request.user)

        message_data['author'] = request.user
        message_data['conversation'] = conversation
        
        message = Message.objects.create(**message_data)

        serializer = ConversationSerializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def delete(self, request, id):
        conversation = Conversation.objects.get(uuid=id)
        conversation.delete()
        return Response({"message": "Conversation deleted successfully."})

    
    def put(self, request, id):
        conversation = Conversation.objects.get(id=id)
        conversation.name = request.data.get('name', conversation.name)  # Fallback to the existing name if not provided
        conversation.save()
        serializer = ConversationSerializer(conversation)
        return Response(serializer.data)
