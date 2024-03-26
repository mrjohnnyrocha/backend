from app.serializers.base import BaseSerializer
from app.serializers.message import MessageSerializer
from app.serializers.user import UserSerializer
from app.models import Conversation
from app.models import Message
from app.models import CustomUser

class ConversationSerializer(BaseSerializer):
    messages = MessageSerializer(many=True)
    members = UserSerializer(many=True)

    class Meta:
        model = Conversation
        fields = '__all__'
        depth = 1
