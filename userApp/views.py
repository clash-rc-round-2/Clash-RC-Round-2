from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login
from django.contrib.auth.models import User
from .models import Question, Submission, UserProfile, MultipleQues
import os


path = os.getcwd()
path1 = path + '/data/usersCode'


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
        os.system('mkdir {}/{}'.format(path1, username))
        login(request, user)
        return redirect(reverse("questionHub"))

    elif request.method == 'GET':
        return render(request, 'userApp/clashlogin.html')


def questionHub(request):
    all_questions = Question.objects.all()
    return render(request, 'userApp/QuestionHub.html', context={'all_questions': all_questions})


def codeSave(request, username, qn):
    if request.method == 'POST':
        user = User.objects.get(username=username)
        content = request.POST['content']
        que = Question.objects.get(pk=qn)
        submission = Submission(code=content, user=user, que=que)
        submission.save()

        try:
            mulQue = MultipleQues.objects.get(user=user, que=que)
        except MultipleQues.DoesNotExist:
            mulQue = MultipleQues(user=user, que=que)

        att = mulQue.attempts

        try:
            os.system('mkdir {}/{}/question{}'.format(path1, username, qn))

        except FileExistsError:
            pass

        codefile = open("{}/{}/question{}/code{}-{}.cpp".format(path1, username, qn, qn, att), "w+")
        codefile.write(content)
        codefile.close()
        mulQue.attempts += 1
        mulQue.save()
        print(mulQue.attempts)
        return redirect("submission", username=username, qn=qn)

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


def submission(request, username, qn):
    user = User.objects.get(username=username)
    que = Question.objects.get(pk=qn)
    allSubmission = Submission.objects.all()
    userQueSub = list()
    for submissions in allSubmission:
        if submissions.que == que and submissions.user == user:
            userQueSub.append(submissions)

    return render(request, 'userApp/submissions.html', context={'allSubmission': userQueSub})


def runCode(request, username, qn):
    user = User.objects.get(username=username)
    que = Question.objects.get(pk=qn)
    mulQue = MultipleQues.objects.get(user=user, que=que)
    attempts = mulQue.attempts
    os.system('python main.py ' + '{}/{}/question{}/code{}-{}.cpp'.format(path1, username, qn, qn, attempts) + ' ' +
              username + ' ' + qn + ' ' + attempts)


def timer():
    # Will Complete this
