from django.utils import timezone
from rest_framework import serializers
import uuid
class BaseSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(default=uuid.uuid4)
    name = serializers.CharField(max_length=100, required=False, default="")
    created_at = serializers.DateTimeField(default=timezone.now)
    updated_at = serializers.DateTimeField(default=timezone.now)


    def validate_uuid(self, value):
        return value
    
    
    