from django.db import models
from app.models.base import BaseModel
from app.models.user import CustomUser
from app.models.conversation import Conversation

class Message(BaseModel):
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.content
