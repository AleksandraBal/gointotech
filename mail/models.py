from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import date

class MailThread(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

    def __str__(self):
        return str(self.sender) + " - " + str(self.receiver)
    
    def get_messages_no(self):
        return self.messages.all().count()
    
    def get_last_message(self):
        return self.messages.latest('sent')

    def get_last_message_date(self):
        last_message = self.messages.latest('sent')
        return last_message.sent

class Message(models.Model):
    thread = models.ForeignKey('MailThread', related_name='messages', on_delete=models.CASCADE, blank=True, null=True)
    sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    body = models.CharField(max_length=2000)
    image = models.ImageField(upload_to='mail_pictures/', blank=True, null=True)    
    document = models.FileField(upload_to='mail_documents/', blank=True, null=True)
    sent = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.body)[:50]