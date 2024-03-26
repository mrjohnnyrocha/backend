from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Message
from app.serializers import MessageSerializer

class MessageAPI(APIView):
    """
    API endpoint that allows messages to be viewed or edited.
    """

    def get(self, request, *args, **kwargs):
        uuid = request.query_params.get("uuid")
        if not uuid:
            return Response({"error": "UUID parameter is missing."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            message = Message.objects.get(uuid=uuid)
            serializer = MessageSerializer(message)
            return Response(serializer.data)
        except Message.DoesNotExist:
            return Response({"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.save()
            return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        uuid = kwargs.get('id')
        try:
            message = Message.objects.get(uuid=uuid)
            message.delete()
            return Response({"message": "Message deleted successfully."})
        except Message.DoesNotExist:
            return Response({"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        uuid = kwargs.get('id')
        try:
            message = Message.objects.get(uuid=uuid)
            serializer = MessageSerializer(message, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Message.DoesNotExist:
            return Response({"error": "Message not found."}, status=status.HTTP_404_NOT_FOUND)
