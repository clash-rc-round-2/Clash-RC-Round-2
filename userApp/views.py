from django.shortcuts import render, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .models import Question, Submission, UserProfile, MultipleQues
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseForbidden
import datetime
import os
import subprocess
import re

from judgeApp.views import exec_main

starttime = 0
end_time = 0
duration = 0
flag = False
start = datetime.datetime(2020, 1, 1, 0, 0)

path_usercode = 'data/usersCode'

NO_OF_QUESTIONS = 6
NO_OF_TEST_CASES = 6


def waiting(request):
    if request.user.is_authenticated:
        return redirect(reverse("questionHub"))
    else:
        global flag
        if not flag:
            return render(request, 'userApp/waiting.html')
        else:
            now = datetime.datetime.now()
            global start
            if now == start:
                return redirect(reverse("signup"))
            elif now > start:
                return redirect(reverse("signup"))
            else:
                return render(request, 'userApp/waiting.html')


def timer(request):
    if request.method == 'GET':
        return render(request, 'userApp/timer.html')

    elif request.method == 'POST':
        global starttime, start
        global end_time
        global duration
        global flag
        flag = True
        duration = 7200  # request.POST.get('duration')
        start = datetime.datetime.now()
        start = start + datetime.timedelta(0, 15)
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
    if request.user.is_authenticated:
        try:
            user = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            user = UserProfile()
    else:
        if request.method == 'POST':
            try:
                username = request.POST.get('username')
                password = request.POST.get('password')
                name1 = request.POST.get('name1')
                name2 = request.POST.get('name2')
                phone1 = request.POST.get('phone1')
                phone2 = request.POST.get('phone2')
                email1 = request.POST.get('email1')
                email2 = request.POST.get('email2')

                if username == "" or password == "":
                    return render(request, 'userApp/login.html')

                user = User.objects.create_user(username=username, password=password)
                userprofile = UserProfile(user=user, name1=name1, name2=name2, phone1=phone1, phone2=phone2, email1=email1,
                                          email2=email2)
                userprofile.save()
                print(username)
                os.system('mkdir {}/{}'.format(path_usercode, username))
                login(request, user)
                return redirect(reverse("instructions"))

            except IntegrityError:
                return render(request, 'userApp/login.html')

            except HttpResponseForbidden:
                return render(request, 'userApp/login.html')

        elif request.method == 'GET':
            return render(request, "userApp/login.html")


def questionHub(request):
    if request.user.is_authenticated:
        try:
            user = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return signup(request)

        all_questions = Question.objects.all()
        all_users = User.objects.all()

        for que in all_questions:
            for user in all_users:
                try:
                    mul_que = MultipleQues.objects.get(user=user, que=que)
                except MultipleQues.DoesNotExist:
                    mul_que = MultipleQues(user=user, que=que)
                que.totalSub += mul_que.attempts
            try:
                que.accuracy = round((que.totalSuccessfulSub * 100/que.totalSub), 1)
            except ZeroDivisionError:
                que.accuracy = 0

        var = calculate()
        if var != 0:
            return render(request, 'userApp/qhub.html', context={'all_questions': all_questions, 'time': var})
        else:
            return render(request, 'userApp/result.html')
    else:
        return HttpResponseRedirect(reverse("signup"))


def codeSave(request, username, qn):
    if request.user.is_authenticated:  # Check Authentication
        if request.method == 'POST':
            que = Question.objects.get(pk=qn)
            user = User.objects.get(username=username)

            content = request.POST['content']
            extension = request.POST['ext']

            user_profile = UserProfile.objects.get(user=user)
            user_profile.choice = extension

            temp_user = UserProfile.objects.get(user=user)
            temp_user.qid = qn
            temp_user.lang = extension
            temp_user.save()

            try:
                mul_que = MultipleQues.objects.get(user=user, que=que)
            except MultipleQues.DoesNotExist:
                mul_que = MultipleQues(user=user, que=que)
                mul_que.save()
            att = mul_que.attempts

            user_question_path = '{}/{}/question{}/'.format(path_usercode, username, qn)

            if not os.path.exists(user_question_path):
                os.system('mkdir ' + user_question_path)

            code_file = user_question_path + "code{}.{}".format(att, extension)

            content = str(content)

            if extension != 'py':
                sandbox_header = '#include"../../../include/sandbox.h"\n'
                try:
                    # Inject the function call for install filters in the user code file
                    # Issue with design this way (look for a better solution (maybe docker))
                    # multiple main strings
                    before_main = content.split('main')[0] + 'main'
                    after_main = content.split('main')[1]
                    index = after_main.find('{') + 1
                    main = before_main + after_main[:index] + 'install_filters();' + after_main[index:]
                    with open(code_file, 'w+') as f:
                        f.write(sandbox_header)
                        f.write(main)
                        f.close()

                except IndexError:
                    with open(code_file, 'w+') as f:
                        f.write(content)
                        f.close()

            else:
                with open(code_file, 'w+') as f:
                    f.write('import temp\n')
                    f.write(content)
                    f.close()

            testcase_values = exec_main(request, qn)
            print(type(testcase_values))

            sub = Submission(code=content, user=user, que=que, attempt=att)
            sub.save()

            mul_que.attempts += 1
            mul_que.save()

            error_text = ""

            epath = path_usercode + '/{}/question{}/error.txt'.format(username, qn)

            if os.path.exists(epath):
                ef = open(epath, 'r')
                error_text = ef.read()
                error_text = re.sub('/.*?:', '', error_text)  # regular expression
                ef.close()

            data = {
                'testcase': testcase_values,
                'error': error_text
            }

            return render(request, 'userApp/testcases.html', context=data)

        elif request.method == 'GET':
            que = Question.objects.get(pk=qn)
            user_profile = UserProfile.objects.get(user=request.user)
            user = User.objects.get(username=username)

            var = calculate()
            if var != 0:
                return render(request, 'userApp/codingPage.html', context={'question': que, 'user': user, 'time': var,
                                                                           'total_score': user_profile.totalScore,
                                                                           'question_id': qn})
            else:
                return render(request, 'userApp/result.html')
    else:
        return HttpResponseRedirect(reverse("signup"))


def instructions(request):
    if request.user.is_authenticated:
        return render(request, 'userApp/instructions.html')
    else:
        return HttpResponseRedirect(reverse("signup"))


def leader(request):
    if request.user.is_authenticated:
        data = {}
        for user in UserProfile.objects.order_by("-totalScore"):
            l = []
            for n in range(1, 7):
                que = Question.objects.get(pk=n)
                try:
                    mulQue = MultipleQues.objects.get(user=user.user, que=que)
                    l.append(mulQue.scoreQuestion)
                except MultipleQues.DoesNotExist:
                    l.append(0)
            l.append(user.totalScore)
            data[user.user] = l

        sorted(data.items(), key=lambda items: (items[1][6], user.latestSubTime))
        var = calculate()
        if var != 0:
            return render(request, 'userApp/leaderboard.html', context={'dict': data, 'range': range(1, 7, 1),
                                                                        'time': var})
        else:
            return render(request, 'userApp/result.html')
    else:
        return HttpResponseRedirect(reverse("signup"))


def submission(request, username, qn):
    user = User.objects.get(username=username)
    print(qn)
    que = Question.objects.get(pk=qn)
    # all_submissions = Submission.objects.filter()
    all_submission = Submission.objects.all()
    userQueSub = list()

    for submissions in all_submission:
        if submissions.que == que and submissions.user == user:
            userQueSub.append(submissions)
    var = calculate()
    print(userQueSub)
    print("working")
    if var != 0:
        return render(request, 'userApp/submissions.html', context={'allSubmission': userQueSub, 'time': var})
    else:
        return render(request, 'userApp/result.html')


def user_logout(request):
    if request.user.is_authenticated:
        try:
            user = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return signup(request)
        object = UserProfile.objects.order_by("-totalScore", "latestSubTime")
        rank = 0
        i = 0
        dict = {}
        for user in object:
            if rank < 3:
                dict[user.user] = user.totalScore
                rank = rank + 1
            else:
                break

        for user in object:
            i += 1
            if str(user.user) == str(request.user.username):
                break

        logout(request)
        return render(request, 'userApp/result.html', context={'dict': dict, 'rank': i, 'name': user.user,
                                                               'score': user.totalScore})
    else:
        return HttpResponseRedirect(reverse("signup"))


def loadBuffer(request):
    username = request.POST.get('username')
    user = UserProfile.objects.get(user=request.user)
    qn = request.POST.get('question_no')
    que = Question.objects.get(pk=qn)
    mul_que = MultipleQues.objects.get(user=user.user, que=que)
    attempts = mul_que.attempts
    ext = request.POST.get('ext')
    response_data = {}

    codeFile = '{}/{}/question{}/code{}.{}'.format(path_usercode, username, qn, attempts - 1, user.lang)

    f = open(codeFile, "r")
    txt = f.read()
    if not txt:
        data = ""
    response_data["txt"] = txt

    return JsonResponse(response_data)


def run(request):
    if request.user.is_authenticated:
        response_data = {}
        username = request.POST.get('username')
        user = UserProfile.objects.get(user=request.user)
        que_no = request.POST.get('question_no')
        ext = request.POST.get('ext')
        code = request.POST.get('content')
        status = str("")
        e_output_file = "{}/data/standard/output/question{}/expected_output1.txt".format(path, que_no)
        expec_out = open(e_output_file, "r")
        expected = expec_out.read()
        expec_out.close()
        actual = str("")

        try:
            os.system('mkdir {}/{}/question{}'.format(path_usercode, username, que_no))
        except FileExistsError:
            pass

        file = open("{}/{}/question{}/sample.{}".format(path_usercode, username, que_no, ext), "w+")
        file.write(code)
        file.close()

        value = subprocess.Popen(["python2", "{}/data/Judge/runcode.py".format(path), path, path_usercode, username,
                                  str(que_no), ext], stdout=subprocess.PIPE)
        (out, err) = value.communicate()

        output = int(out)
        if output == 10:
            status = "Correct answer"
            user_out_file = '{}/{}/question{}/sample_out.txt'.format(path_usercode, username, que_no)
            user_out = open(user_out_file, "r")
            actual = user_out.read()
            user_out.close()
        elif output == 20:
            status = "Wrong Answer"
            user_out_file = '{}/{}/question{}/sample_out.txt'.format(path_usercode, username, que_no)
            user_out = open(user_out_file, "r")
            actual = user_out.read()
            user_out.close()
        elif output == 30:
            status = "Time limit exceed"
        elif output == 40:
            err_file = "{}/{}/question{}/error.txt".format(path_usercode, username, que_no)
            error = open(err_file, "r")
            error_text = error.read()
            status = re.sub('/.*?:', '', error_text)
            error.close()
        elif output == 50:
            status = "Run time error : core dumped"
        elif output == 60:
            status = "Abnormal termination"

        response_data["status"] = status
        response_data["actual"] = actual
        response_data["expected"] = expected

        return JsonResponse(response_data)

    else:
        return HttpResponseRedirect(reverse("signup"))


def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    if data['is_taken']:
        data['error_message'] = 'username already exits.'

    return JsonResponse(data)
