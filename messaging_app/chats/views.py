from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer


# ======================================
# CONVERSATION VIEWSET
# ======================================
class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    @action(detail=False, methods=['post'])
    def create_conversation(self, request):
        """
        Create a conversation with a list of participants.
        Expected JSON:
        {
            "participants": ["uuid1", "uuid2"]
        }
        """
        participant_ids = request.data.get("participants", [])

        if len(participant_ids) < 2:
            return Response(
                {"error": "A conversation requires at least 2 participants."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participant_ids)
        conversation.save()

        return Response(
            ConversationSerializer(conversation).data,
            status=status.HTTP_201_CREATED
        )


# ======================================
# MESSAGE VIEWSET
# ======================================
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    @action(detail=False, methods=['post'])
    def send_message(self, request):
        """
        Send a message inside an existing conversation.
        Expected JSON:
        {
            "conversation": "<conversation_uuid>",
            "sender": "<sender_uuid>",
            "message_body": "Hello"
        }
        """
        conversation_id = request.data.get("conversation")
        sender_id = request.data.get("sender")
        message_body = request.data.get("message_body")

        if not conversation_id or not sender_id or not message_body:
            return Response(
                {"error": "conversation, sender and message_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate conversation
        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"error": "Conversation not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Validate sender
        try:
            sender = User.objects.get(id=sender_id)
        except User.DoesNotExist:
            return Response(
                {"error": "Sender not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Confirm sender is part of the conversation
        if sender not in conversation.participants.all():
            return Response(
                {"error": "Sender is not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        # Create the message
        message = Message.objects.create(
            conversation=conversation,
            sender=sender,
            message_body=message_body
        )

        return Response(
            MessageSerializer(message).data,
            status=status.HTTP_201_CREATED
        )



