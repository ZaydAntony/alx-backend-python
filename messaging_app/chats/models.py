from django.db import models

# Create your models here.

import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# ==============================
# CUSTOM USER MODEL
# ==============================

class User(AbstractUser):
    
    #Custom User model extending Django's AbstractUser.
    #Adds UUID primary key, phone number, and role.
    

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)

    phone_number = models.CharField(max_length=20, null=True, blank=True)

    ROLE_CHOICES = [
        ('guest', 'Guest'),
        ('host', 'Host'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guest')

    created_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.username} ({self.email})"


# ==============================
# CONVERSATION MODEL
# ==============================

class Conversation(models.Model):
    
    #A conversation contains 2+ participants.
    

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    participants = models.ManyToManyField(User, related_name="conversations")

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id}"


# ==============================
# MESSAGE MODEL
# ==============================

class Message(models.Model):
    
    #Messages belong to a conversation and have one sender.
    

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_messages"
    )

    message_body = models.TextField()

    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message {self.id} from {self.sender.username}"
