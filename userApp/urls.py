from django.urls import path
from . import views
from django.views.decorators.cache import never_cache

urlpatterns = [
    path('instructions', views.instructions, name='instructions'),
    path('', views.signup, name='signup'),
    path('leaderboard', views.leader, name='leader'),
    path('timer/', views.timer, name='timer'),
    path('user/allque', views.questionHub, name='questionHub'),
    path('user/<username>/<int:qn>', views.codeSave, name='codeSave'),
    path('user/<username>/<int:qn>/submission', views.submission, name='submission'),
    path('user/<username>/<int:qn>/testCases', views.runCode, name='runCode'),
]
