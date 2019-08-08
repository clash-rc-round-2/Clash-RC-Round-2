from django.db import models


class UserProfile(models.Model):
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    score = models.IntegerField(default=0)

    def __str__(self):
            return self.username


class Question(models.Model):
    title_number = models.CharField(max_length=50)
    question = models.CharField(max_length=5000)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
            return self.title_number + '-' + self.question


class Submission(models.Model):
    time = models.DateTimeField()
    input = models.CharField(max_length=1000)
    output = models.CharField(max_length=100)
    que = models.ForeignKey(Question, on_delete=models.CASCADE)
