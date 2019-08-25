from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Question, Submission, UserProfile, MultipleQues
from django.http import Http404
import os, subprocess
import array

cwd = os.getcwd()
n = 0


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
        userprofile.save()
        os.chdir('%s/data/usersCode' % cwd)
        os.mkdir(username)
        login(request, user)
        return redirect(reverse("detail"))

    elif request.method == 'GET':
        return render(request, 'userApp/clashlogin.html')


def detail(request):
    all_questions = Question.objects.all()
    return render(request, 'userApp/QuestionHub.html', context={'all_questions': all_questions})


def file(request, username, qn):
    if request.method == 'POST':
        user = User.objects.get(username=username)
        content = request.POST['content']
        question = Question.objects.get(pk=qn)
        att = question.attempt
        submission = Submission(code=content, user=user, que=question)
        submission.save()
        os.chdir(cwd + '/data/usersCode/' + username)

        try:
            mulQue = MultipleQues.objects.get(user=user, que=question)
        except MultipleQues.DoesNotExist:
            mulQue = MultipleQues(user=user, que=question)
        mulQue.save()
        att = mulQue.attempts

        try:
            os.mkdir('question' + str(qn))
        except FileExistsError:
            pass

        os.chdir('question' + str(qn) + '/')
        path = os.getcwd()
        codefile = open('code' + str(qn) + '.' + str(att) + '.cpp', "w+")
        codefile.write(content)
        codefile.close()
        question.attempt += 1
        question.save()
        print(question.attempt)
        p = subprocess.Popen("python main.py", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             shell=True)
        in1 = str(path)
        in1.encode('utf-8')
        p.communicate(bytes(in1, 'utf-8'))
        p.wait()
        return redirect(reverse("detail"))

    elif request.method == 'GET':
        question = Question.objects.get(pk=qn)
        user = User.objects.get(username=username)
        return render(request, 'userApp/codingPage.html', context={'question': question, 'user': user})


def instructions(request):
    return render(request, 'userApp/instpgclash.html')


def leader(request):
    dict = {}
    for user in UserProfile.objects.all():
        list = []
        for n in range(1, 7):
            que = Question.objects.get(pk=n)
            try:
                mulQue = MultipleQues.objects.get(user=user.user, que=que)
                list.append(mulQue.scoreQuestion)
            except MultipleQues.DoesNotExist:
                list.append(0)
        list.append(user.totalScore)
        dict[user.user] = list

    print(dict)
    sorted(dict.items(), key=lambda items: items[1][6])
    return render(request, 'userApp/leaderboard_RC(blue).html', context={'dict': dict})

