from rest_framework.views import APIView
from django.db import models
from django.utils import timezone
import uuid

class BaseAPI(APIView): 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    

    class Meta:
        abstract = True
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

    