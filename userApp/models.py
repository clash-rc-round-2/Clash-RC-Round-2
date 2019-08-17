from django.db import models
from django.contrib.auth.models import User

NO_OF_QUESTIONS = 6


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    totalScore = models.IntegerField(default=0)
    email1 = models.EmailField(default='example@gmail.com')
    email2 = models.EmailField(default='example@gmail.com')
    phone1 = models.CharField(max_length=10)
    phone2 = models.CharField(max_length=10)
    name1 = models.CharField(max_length=100)
    name2 = models.CharField(max_length=100)
    latestSubTime = models.TimeField(default='00:00')

    def __str__(self):
            return self.user.username


class Question(models.Model):
    title_number = models.CharField(max_length=50)
    attempt = models.IntegerField(default=0)
    question = models.CharField(max_length=5000)
    totalSub = models.IntegerField(default=0)
    totalSuccessfulSub = models.IntegerField(default=0)
    accuracy = models.IntegerField(default=0)           # accuracy = total Successful submission / total Submission

    def __str__(self):
            return self.title_number + '-' + self.question


class MultipleQues(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    scoreQuestion = models.IntegerField(default=0)
    attempts = models.IntegerField(default=0)


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    que = models.ForeignKey(Question, on_delete=models.CASCADE)
    code = models.CharField(max_length=1000)
    subStatus = models.BooleanField(default=False)           # False for wrong submission and True for Correct
    subTime = models.TimeField(default='00:00')
    subScore = models.IntegerField(default=0)

    def __str__(self):
            return self.user.username + ' - ' + self.que.title_number
