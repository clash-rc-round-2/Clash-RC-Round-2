from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Question
import subprocess
import os


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        cwd = os.getcwd()
        os.chdir('%s/data/usersCode'%cwd)
        os.mkdir(username)
        login(request, user)
        return redirect(reverse("detail"))

    elif request.method == 'GET':
        return render(request, 'userApp/signup.html')


def detail(request):
    all_questions = Question.objects.all()
    return render(request, 'userApp/loggedin.html', context={'all_questions': all_questions})


def file(request, qn):
    if request.method == 'POST':
       # username = User.username
        content = request.POST['content']
        #cwd = os.getcwd()
        #os.chdir('%s/data/usersCode/%s'%(cwd,username))
        f = open("solution.cpp","w+")
        f.write(content)
        f.close()
        return redirect(reverse("detail"))

    elif request.method == 'GET':
        question = Question.objects.get(pk=qn)
        return render(request, 'userApp/question.html', context={'question': question})
