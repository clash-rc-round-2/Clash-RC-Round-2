from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import Question, Submission, UserProfile, MultipleQues
from django.http import HttpResponse
import datetime
import os

global starttime
global end_time

path = os.getcwd()
path_usercode = path + '/data/usersCode'

NO_OF_QUESTIONS = 6

def timer(request):
    if request.method == 'GET':
        return render(request, 'userApp/timer.html')

    elif request.method == 'POST':
        global starttime
        global end_time
        start = datetime.datetime.now()
        time = start.second + start.minute * 60 + start.hour * 60 * 60
        starttime = time
        end_time = time + 7200
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
        user = User.objects.create_user(username=username, password=password)
        userprofile = UserProfile(user=user, name1=name1, name2=name2, phone1=phone1, phone2=phone2, email1=email1,
                                  email2=email2)
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
        extension = request.POST['ext']

        que = Question.objects.get(pk=qn)
        submission = Submission(code=content, user=user, que=que, choice=extension)
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

    os.popen('python2 data/Judge/main.py ' + '{}/{}/question{}/code{}-{}.cpp'.format(path_usercode, username, qn, qn,
             attempts-1) + ' ' + username + ' ' + str(qn))

    total_out_path = path_usercode + '/{}/question{}'.format(username, qn)
    print(total_out_path)
    total_file = open('{}/total_output.txt'.format(total_out_path), 'r')

    # code will have text in form '1020301020'
    # output_list will contain (10, 20 , 30, 10, 20)  for 5 test cases

    code = int(total_file.readline()[::-1])       # This will reverse the Code
    output_list = list()

    for i in range(0, NO_OF_QUESTIONS):
        var = code % 100
        # output_list.append(var)
        code = code / 100

    '''
        Sandbox will return(save) these values in total_output.txt
        10 = right answer (PASS)
        20 = wrong answer (FAIL)
        30 = TLE
        40 = compile time error (CLE)
    '''

    com_time_error = False                 # For Compile time error for all program

    for i in output_list:
        if i == 40:
            com_time_error = True

    if com_time_error:
        for i in output_list:
            i = 40
        error_path = path_usercode + '/{}/question{}'.format(username, qn)
        error_file = open('{}/error.txt'.format(error_path), 'r')

    return render(request, 'userApp/TestCases 111.html')


def user_logout(request):
    logout(request)
    return render(request, 'userApp/clash result blue.html')
