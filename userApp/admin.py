from django.contrib import admin
from .models import User, Question, Submission

admin.site.register(Question)
admin.site.register(User)
admin.site.register(Submission)
