from django.urls import path
from . import views

urlpatterns = [
    path('', views.instructions, name='instructions'),
    path('signup', views.signup, name='signup'),
    path('leaderboard', views.leader, name='leader'),
    path('user/allque', views.detail, name='detail'),
    path('user/<username>/<int:qn>', views.file, name='file'),
    path('user/<username>/<int:qn>/submission', views.submission, name='submission'),
]
