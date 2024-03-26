from app.models.base import BaseModel
from django.db import models

class Conversation(BaseModel):
    members = models.ManyToManyField('CustomUser', related_name='conversations')
   
    def __str__(self):
        return self.name