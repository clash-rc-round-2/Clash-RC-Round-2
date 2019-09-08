from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import Question, Submission, UserProfile, MultipleQues
from django.http import HttpResponse,JsonResponse
import datetime
import os

global starttime
global end_time
global duration

path = os.getcwd()
path_usercode = path + '/data/usersCode'

NO_OF_QUESTIONS = 6
NO_OF_TEST_CASES = 6


def timer(request):
    if request.method == 'GET':
        return render(request, 'userApp/timer.html')

    elif request.method == 'POST':
        global starttime
        global end_time
        global duration
        duration = request.POST.get('duration')
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
        user = User.objects.create_user(username=username, password=password)
        userprofile = UserProfile(user=user, name1=name1, name2=name2, phone1=phone1, phone2=phone2, email1=email1,
                                  email2=email2)
        userprofile.save()
        os.system('mkdir {}/{}'.format(path_usercode, username))
        login(request, user)
        return redirect(reverse("questionHub"))

    elif request.method == 'GET':
        return render(request, "userApp/clashlogin.html")


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

        user_profile = UserProfile.objects.get(user=user)
        user_profile.choice = extension

        que = Question.objects.get(pk=qn)

        temp_user = UserProfile.objects.get(user=user)
        temp_user.qid = qn
        temp_user.save()

        submission = Submission(code=content, user=user, que=que)
        submission.save()

        try:
            mul_que = MultipleQues.objects.get(user=user, que=que)
        except MultipleQues.DoesNotExist:
            mul_que = MultipleQues(user=user, que=que)

        att = mul_que.attempts

        try:
            os.system('mkdir {}/{}/question{}'.format(path_usercode, username, qn))

        except FileExistsError:
            pass

        codefile = open("{}/{}/question{}/code{}-{}.{}".format(path_usercode, username, qn, qn, att, extension), "w+")
        codefile.write(content)
        codefile.close()
        mul_que.attempts += 1
        mul_que.save()
        print(mul_que.attempts)
        return redirect("runCode", username=username, qn=qn)

    elif request.method == 'GET':
        question = Question.objects.get(pk=qn)
        user = User.objects.get(username=username)
        return render(request, 'userApp/codingPage.html', context={'question': question, 'user': user})


def instructions(request):
    return render(request, 'userApp/QuestionHub.html')


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
    user_profile = UserProfile.objects.get(user=user)
    que = Question.objects.get(pk=qn)
    mul_que = MultipleQues.objects.get(user=user, que=que)
    attempts = mul_que.attempts
    submission = Submission.objects.get(user=user, que=que)

    os.popen('python2 data/Judge/main.py ' + '{}/{}/question{}/code{}-{}.{}'.format(path_usercode, username, qn, qn,
             attempts-1, user_profile.choice) + ' ' + username + ' ' + str(qn))

    total_out_path = path_usercode + '/{}/question{}'.format(username, qn)
    print(total_out_path)
    total_file = open('{}/total_output.txt'.format(total_out_path), 'r')
    code = int(total_file.readline()[::-1])       # This will reverse the Code

    '''
        code will have text in form '1020301020'
        output_list will contain (10, 20, 30, 10, 20)  for 5 test cases

        Sandbox will return(save) these values in total_output.txt
        10 = right answer (PASS)
        20 = wrong answer (WA)
        30 = Time Limit Exceed (TLE)
        40 = compile time error (CTE)
    '''

    output_list = list()
    correct_list = list()

    for i in range(0, NO_OF_TEST_CASES):
        correct_list.append('PASS')               # list of all PASS test Cases

    for i in range(0, NO_OF_TEST_CASES):
        var = code % 100
        if var == 10:
            output_list.append('PASS')
        elif var == 20:
            output_list.append('WA')
        elif var == 30:
            output_list.append('TLE')
        elif var == 40:
            output_list.append('CTE')
        code = code / 100

    if output_list == correct_list:
        mul_que.scoreQuestion = 100

    com_time_error = False
    tle_error = False
    wrg_ans = False

    for i in output_list:
        if i == 40:
            com_time_error = True
            submission.subStatus = 'CTE'
        elif i == 30:
            tle_error = True
            submission.subStatus = 'TLE'
        elif i == 20:
            wrg_ans = True
            submission.subStatus = 'WA'

    if com_time_error:
        for i in output_list:                  # assigning each element with 40 (CTE will be for every test case)
            i = 40
        error_path = path_usercode + '/{}/question{}'.format(username, qn)
        error_file = open('{}/error.txt'.format(error_path), 'r')

    dict = {'com_status': submission.subStatus, 'output_list': output_list}

    return render(request, 'userApp/TestCases 111.html', dict)


def user_logout(request):
    logout(request)
    return render(request, 'userApp/clash result blue.html')


def loadBuffer(request):
    username = request.user.username
    user = UserProfile.objects.get(user=request.user)
    que = Question.objects.get(pk=user.qid)
    mul_que = MultipleQues.objects.get(user=user.user, que=que)
    attempts = mul_que.attempts
    qn = user.qid
    response_data = {}

    codeFile = '{}/{}/question{}/code{}-{}.{}'.format(path_usercode, username, qn, qn, attempts - 2, user.choice)

    f = open(codeFile, "r")
    txt = f.read()

    if not txt:
        data = ""
    response_data["txt"] = txt

    return JsonResponse(response_data)
