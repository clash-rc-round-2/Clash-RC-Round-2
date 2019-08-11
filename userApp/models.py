from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    # time = models.DateTimeField()

    def __str__(self):
            return self.user.username


class Question(models.Model):
    title_number = models.CharField(max_length=50)
    question = models.CharField(max_length=5000)

    def __str__(self):
            return self.title_number + '-' + self.question


class Submission(models.Model):
    code = models.CharField(max_length=1000, default="")
    # output = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=UserProfile(user=User()))
