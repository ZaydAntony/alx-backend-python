# chats/permissions.py
from rest_framework.permissions import BasePermission


class IsConversationParticipant(BasePermission):
    """
    Allows access only to conversation participants.
    """

    def has_object_permission(self, request, view, obj):
        # obj is a Conversation instance
        return request.user in obj.participants.all()


class IsMessageOwner(BasePermission):
    """
    Allows access only to users who sent or received the message.
    """

    def has_object_permission(self, request, view, obj):
        # obj is a Message instance
        return request.user == obj.sender or request.user in obj.conversation.participants.all()
