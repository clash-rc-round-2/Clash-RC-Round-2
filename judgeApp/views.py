import os
from userApp.models import UserProfile, MultipleQues, Question
from .main import run_in_sandbox

TESTCASES_NO = 6

path_main = 'judgeApp'
path_users_code = 'data/usersCode/'
standard_data = 'data/standard/'


def clean_up(user_que_path):
    items = ['temp.py', 'error.txt', 'exe']

    for i in items:
        fp = user_que_path + i
        if os.path.exists(fp):
            os.system('rm ' + fp)

    # use regex here (learn it)
    for i in range(TESTCASES_NO):
        os.system('rm ' + user_que_path + 'output{}.txt'.format(i + 1))


def get_signals_dict():
    signals = {
        0: 'A.C',  # Correct ans
        1: 'C.T.E',  # compile time error
        -31: 'A.T',
        159: 'A.T',  # System code
        135: 'M.E',  # Memory exceeded
        136: 'R.T.E',  # Divide by zero
        139: 'R.T.E',  # sigv
        -9: 'T.L.E',
        137: 'T.L.E',  # Time limit exceeded
        'wa': 'W.A',  # Wrong answer
        127: 'unknown error',
    }

    return signals


def compare(user_out, e_out):
    user = open(user_out)
    expected = open(e_out)

    lines_user = user.readlines()
    l1 = [i.strip() for i in lines_user]
    lines_expected = expected.readlines()
    l2 = [i.strip() for i in lines_expected]
    flag = 0
    if len(l1) == len(l2):
        for i in range(len(l1)):  # check if files of equal length
            if l1[i] == l2[i]:
                flag = 1
            else:
                break
        if flag:
            return 0
        else:
            return 'wa'
    return 'wa'


def run_test_case(test_case_no, user_que_path, code_file_path, lang, qno):
    input_file = standard_data + 'input/question{}/input{}.txt'.format(qno, test_case_no)
    input_f = open(input_file, "r")  # standard input

    user_out_file = user_que_path + 'output{}.txt'.format(test_case_no)
    user_out_f = os.open(user_out_file, os.O_RDWR | os.O_CREAT)  # user's output

    error_file = user_que_path + "error.txt"
    err_f = open(error_file, 'w+')

    if lang == 'py':
        exec_file = code_file_path
    else:
        exec_file = user_que_path + 'exe'

    process_code = run_in_sandbox(exec_file, lang, input_f, user_out_f, err_f)

    input_f.close()
    err_f.close()
    os.close(user_out_f)

    e_output_file = standard_data + 'output/question{}/expected_output{}.txt'.format(qno, test_case_no)

    if process_code == 0:
        result_value = compare(user_out_file, e_output_file)
        return result_value

    return process_code


def compile_code(user_question_path, code_file_path, err_file):
    lang = code_file_path.split('.')[1]
    if lang == 'c':
        rc = os.system(
            "gcc" + " -o " + user_question_path + 'exe ' + code_file_path + ' -lseccomp ' + '-lm 2>' + err_file)
    else:
        rc = os.system(
            "g++" + " -o " + user_question_path + 'exe ' + code_file_path + ' -lseccomp ' + '-lm 2>' + err_file)

    return rc  # return 0 for success and 1 for error


def exec_main(request, qno):
    pro_user = UserProfile.objects.get(user=request.user)
    q = Question.objects.get(pk=qno)
    que = MultipleQues.objects.get(user=pro_user.user, que=q)
    user = pro_user.user

    user_question_path = path_users_code + '{}/question{}/'.format(user.username, qno)
    code_file_path = user_question_path + 'code{}.{}'.format(que.attempts, pro_user.lang)

    sandbox_file_py = 'data/include/pysand.py'

    signals = get_signals_dict()

    # Make a temporary sandbox file to import for the current code (A better soltion is relative imports)
    # Implement it later
    with open(user_question_path + 'temp.py', 'w+') as f:
        sand = open(sandbox_file_py, 'r')
        f.write(sand.read())
        sand.close()
        f.close()

    error_file = user_question_path + "error.txt"

    result = []

    if pro_user.lang != 'py':
        # Compile only if c or cpp
        return_value = compile_code(user_question_path, code_file_path, error_file)  # calling compile()

        if return_value == 1:
            result = ["C.T.E"] * 6
            clean_up(user_question_path)
            return result

    for i in range(TESTCASES_NO):
        process_code = run_test_case(i + 1, user_question_path, code_file_path, pro_user.lang, qno)
        result.append(signals[process_code])

    clean_up(user_question_path)

    return result
