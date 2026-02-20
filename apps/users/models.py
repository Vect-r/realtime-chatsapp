from django.db import models
from apps.master.models import BaseClass
from django.utils import timezone

# Create your models here.
class User(BaseClass):
    username = models.CharField(null=False,blank=False,max_length=255)
    password = models.CharField(null=False,blank=False,max_length=255)
    email = models.EmailField(null=False,blank=False,max_length=255)
    isActive = models.BooleanField(default=False)
    bio = models.TextField(max_length=200)

    def __str__(self):
        return f"{self.username} -> {self.email}"

class Conversation(BaseClass):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations_started")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations_received")

    class Meta:
        unique_together = ('user1', 'user2')

    def __str__(self):
        return f"{self.user1.username} ↔ {self.user2.username}"

    def get_other_user(self, current_user):
        return self.user2 if self.user1 == current_user else self.user1
    
class Message(BaseClass):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"

def get_or_create_conversation(user_a, user_b):
    user1, user2 = sorted([user_a, user_b], key=lambda u: u.id)
    convo, created = Conversation.objects.get_or_create(user1=user1, user2=user2)
    return convo
