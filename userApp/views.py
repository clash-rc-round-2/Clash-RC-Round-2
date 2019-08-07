from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import QUESTION


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect(reverse("detail"))

    elif request.method == 'GET':
        return render(request, 'userApp/signup.html')


def detail(request):
    all_questions = QUESTION.objects.all()
    return render(request, 'userApp/loggedin.html', context={'all_questions': all_questions})


def file(request, qn):
    question = QUESTION.objects.get(pk=qn)
    return render(request, 'userApp/question.html', context={'question': question})
