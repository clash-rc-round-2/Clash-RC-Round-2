from django.contrib import admin
from .models import UserProfile, Question, Submission

admin.site.register(Question)
admin.site.register(UserProfile)
admin.site.register(Submission)
