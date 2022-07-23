from django.db import models
from django.utils import timezone
from accounts.models import Student, Supervisor, User
from django.urls import reverse

MULTICHOICE = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
)




class Log(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='logs')
    document = models.FileField(upload_to='documents/')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    approved_for_academic = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('assessments:detail', args=[self.id])

    class Meta:
        ordering = ('-created',)


class Comment(models.Model):
    log = models.ForeignKey(Log, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_comments')
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)



class Message(models.Model):
    message_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_from')
    message_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_to')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created',)



