from django.db import models
from django.contrib.auth.models import User


class User(models.Model):
    score = models.IntegerField(default=0)

    def __str__(self):
            return self.username


class Question(models.Model):
    title_number = models.CharField(max_length=50)
    question = models.CharField(max_length=5000)

    def __str__(self):
            return self.title_number + '-' + self.question


class Submission(models.Model):
    time = models.DateTimeField()
    code = models.CharField(max_length=1000)
    output = models.CharField(max_length=100)
    que = models.ForeignKey(Question, on_delete=models.CASCADE)
