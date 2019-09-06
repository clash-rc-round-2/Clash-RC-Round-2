from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login,logout
from django.contrib.auth.models import User
from .models import Question, Submission, UserProfile, MultipleQues
from django.http import HttpResponse
import datetime
import os

global starttime
global end_time
global duration

path = os.getcwd()
path_usercode = path + '/data/usersCode'


def timer(request):
    if request.method == 'GET':
        return render(request, 'userApp/timer.html')

    elif request.method == 'POST':
        global duration
        global starttime
        global end_time
        duration=request.POST.get('duration')
        start = datetime.datetime.now()
        time = start.second + start.minute * 60 + start.hour * 60 * 60
        starttime = time
        end_time = time + int(duration)
        return HttpResponse(" time is set ")


def calculate():
    time = datetime.datetime.now()
    nowsec = (time.hour * 60 * 60) + (time.minute * 60) + time.second
    global starttime
    global end_time
    diff = end_time - nowsec
    if nowsec < end_time:
        return diff
    else:
        return 0


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
        junior = request.POST.get('junior')

        if request.POST.get('junior') == 'junior':
            juniorT = True
        else:
            juniorT = False

        user = User.objects.create_user(username=username, password=password)
        userprofile = UserProfile(user=user, name1=name1, name2=name2, phone1=phone1, phone2=phone2, email1=email1,
                                  email2=email2, junior=juniorT)
        userprofile.save()
        os.system('mkdir {}/{}'.format(path_usercode, username))
        login(request, user)
        return redirect(reverse("questionHub"))

    elif request.method == 'GET':
        return render(request, 'userApp/clashlogin.html')


def questionHub(request):
    all_questions = Question.objects.all()
    var = calculate()
    if var != 0:
        return render(request, 'userApp/QuestionHub.html', context={'all_questions': all_questions, 'time': var})
    else:
        return render(request, 'userApp/final.html')


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
            os.system('mkdir {}/{}/question{}'.format(path_usercode, username, qn))

        except FileExistsError:
            pass

        codefile = open("{}/{}/question{}/code{}-{}.cpp".format(path_usercode, username, qn, qn, att), "w+")
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
    return render(request, 'userApp/leaderboard_RC(blue).html', context={'dict': dict, 'range': range(1, 7, 1)})


def submission(request, username, qn):
    user = User.objects.get(username=username)
    que = Question.objects.get(pk=qn)
    allSubmission = Submission.objects.all()
    userQueSub = list()
    for submissions in allSubmission:
        if submissions.que == que and submissions.user == user:
            userQueSub.append(submissions)
    var = calculate()
    if var != 0:
        return render(request, 'userApp/submissions.html', context={'allSubmission': userQueSub, 'time': var})
    else:
        return render(request, 'userApp/final.html')


def runCode(request, username, qn):
    user = User.objects.get(username=username)
    que = Question.objects.get(pk=qn)
    mulQue = MultipleQues.objects.get(user=user, que=que)
    attempts = mulQue.attempts
    extension = UserProfile.objects.get(user=user).choice

    print('python data/Judge/main.py ' + '{}/{}/question{}/code{}-{}.cpp'.format(path_usercode, username, qn, qn
             , attempts-1) + ' ' + username + ' ' + str(qn))

    os.popen('python data/Judge/main.py ' + '{}/{}/question{}/code{}-{}.cpp'.format(path_usercode, username, qn, qn
             , attempts-1) + ' ' + username + ' ' + str(qn))

    total_out_path = path_usercode + '/{}/question{}'.format(username, qn)
    print(total_out_path)
    total_file = open('{}/total_output.txt'.format(total_out_path), 'r')

    code = total_file.readline()

    if code == "11111":
        mulQue.scoreQuestion += 4
    else:
        mulQue.scoreQuestion -= 2

    return render(request, 'userApp/TestCases 111.html')


def user_logout(request):
    user = MultipleQues.objects.get(user=request.user)
    object =  MultipleQues.objects.order_by("scoreQuestion")
    rank = 0
    for n in object:
        rank += 1
        if str(n.user.username) == str(request.user.username):
            break

    dict = {'rank': rank, 'name': request.user.username, 'score': n.scoreQuestion}
    logout(request)
    return render(request,  'userApp/clash result blue2.html', context=dict)

