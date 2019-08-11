from django.contrib import admin
from .models import Question, Submission, UserProfile

admin.site.register(Question)
admin.site.register(Submission)
admin.site.register(UserProfile)
