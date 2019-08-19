from django.urls import path
from . import views

urlpatterns = [
    path('', views.instruct, name='instruct'),
    path('signup', views.signup, name='signup'),
    path('user/allque', views.detail, name='detail'),
    path('user/<username>/<int:qn>', views.file, name='file'),
 #   path('user',views.instructions,name='instructions')
]
