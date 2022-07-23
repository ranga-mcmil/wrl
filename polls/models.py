import datetime
from operator import mod
from random import choices
from accounts.models import User

from django.db import models
from django.utils import timezone

class Questionnare(models.Model):
    taker = models.CharField(max_length=200)

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now()
datetime.timedelta(days=1)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class Survey(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='survey')
    answer = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='my_survey')
    qustionnare = models.ForeignKey(Questionnare, on_delete=models.CASCADE, related_name='survey', blank=True, null=True)


class StudentName(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Remark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.TextField()

class StudentRemark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    remarks = models.TextField()

