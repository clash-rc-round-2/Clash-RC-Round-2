from django.db import models


class QUESTION(models.Model):
    title_number = models.CharField(max_length=50)
    question = models.CharField(max_length=5000)

    def __str__(self):
            return self.title_number + '-' + self.question


class UserProfile(models.Model):
    username = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
