from django.urls import path
from . import views

urlpatterns = [
    path('', views.signup, name='signup'),
    path('user_app/li', views.detail, name='detail'),
    path('user_app/qp/<int:qn>', views.file, name='file'),
]
