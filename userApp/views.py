from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Question, Submission, UserProfile
import os

cwd = os.getcwd()


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name1 = request.POST.get('name1')
        name2 = request.POST.get('name2')
        phone1 = request.POST.get('phone1')
        phone2 = request.POST.get('phone2')
        email1 = request.POST.get('email1')
        email2 = request.POST.get('email2')
        user = User.objects.create_user(username=username, password=password)
        userprofile = UserProfile(user=user, name1=name1, name2=name2, phone1=phone1, phone2=phone2, email1=email1,
                                  email2=email2)
        os.chdir('%s/data/usersCode' % cwd)
        os.mkdir(username)
        login(request, user)
        return redirect(reverse("detail"))

    elif request.method == 'GET':
        return render(request, 'userApp/clashlogin.html')


def detail(request):
    all_questions = Question.objects.all()
    return render(request, 'userApp/loggedin.html', context={'all_questions': all_questions})


def file(request, username, qn):
    if request.method == 'POST':
        user = User.objects.get(username=username)
        content = request.POST['content']
        question = Question.objects.get(pk=qn)
        att = question.attempt
        submission = Submission(code=content, user=user, que=question)
        submission.save()
        os.chdir(f'{cwd}/data/usersCode/{username}')

        try:
            os.mkdir(f'question{qn}')
        except(FileExistsError):
            pass

        os.chdir(f'question{qn}/')
        codefile = open(f"code{qn}.{att}.cpp", "w+")
        codefile.write(content)
        codefile.close()
        question.attempt += 1
        question.save()
        print(question.attempt)
        return redirect(reverse("detail"))

    elif request.method == 'GET':
        question = Question.objects.get(pk=qn)
        user = User.objects.get(username=username)
        return render(request, 'userApp/question.html', context={'question': question, 'user': user})
