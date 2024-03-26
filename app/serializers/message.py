from rest_framework import serializers
from app.models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'  # Adjust fields according to your model

    def create(self, validated_data):
        # Create and return a new `Message` instance, given the validated data.
        return Message.objects.create(**validated_data)
