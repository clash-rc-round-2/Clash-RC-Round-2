from django.db import models


class QUESTION(models.Model):
    title_number = models.CharField(max_length=50)
    question = models.CharField(max_length=500)

    def __str__(self):
            return self.title_number + '-' + self.question
