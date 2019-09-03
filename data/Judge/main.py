import os
import sys
from sandbox import *

NO_OF_QUESTIONS = 6

# paths
path = os.getcwd()    # 'clash'
path_userCode = path + '/data/usersCode'
input_path = path + '/data/standard/input'
output_path = path + '/data/standard/output'


try:
    # check platform type
    system, machine = os.uname()[0], os.uname()[4]
    if system not in ('Linux',) or machine not in ('i686', 'x86_64',):
        raise AssertionError("Unsupported platform type.\n")
    # check package availability / version
    import sandbox

    if not hasattr(sandbox, '__version__') or sandbox.__version__ < "0.3.4-3":
        raise AssertionError("Unsupported sandbox version.\n")
    from sandbox import *
except ImportError:
    sys.stderr.write("Required package(s) missing.\n")
    sys.exit(os.EX_UNAVAILABLE)
except AssertionError as e:
    sys.stderr.write(str(e))
    sys.exit(os.EX_UNAVAILABLE)


def config_sandbox(targeted_file, input_file, out_file):
    # sandbox configuration
    cookbook = {
        'args': targeted_file,          # targeted program
        'stdin': input_file,            # input to targeted program
        'stdout': out_file,             # output from targeted program
        'stderr': sys.stderr,           # error from targeted program
        'quota': dict(wallclock=30000,  # 30 sec
                      cpu=2000,         # 2 sec
                      memory=8388608,   # 8 MB
                      disk=1048576)}    # 1 MB
    # create a sandbox instance and execute till end
    msb = Sandbox(**cookbook)
    msb.run()
    d = Sandbox.probe(msb)
    d['cpu'] = d['cpu_info'][0]
    d['mem'] = d['mem_info'][1]
    d['result'] = msb.result
    return msb.result                 # return 1 if complied successfully..


def compile(filename, extension):
    return_value = 1         # By default error while running file.
    if extension == 'c':
        return_value = os.system('gcc ' + '-o ' + '{} '.format(filename) +
                                 path + '/{}.c'.format(filename))

    elif extension == 'cpp':
        return_value = os.system('g++ ' + '-o ' + '{} '.format(filename) +
                                 path + '/{}.cpp'.format(filename))

    return return_value      # return 0 for success and 1 for error


def compare(user_out, e_out):
    user = open(user_out)
    expected = open(e_out)

    lines_user = user.readline()
    lines_expected = expected.readline()

    same = True                                     # False if not same else True

    for i in range(len(lines_expected)):
        if lines_expected[i] != lines_user[i]:
            same = False

    return same


def run_test_cases(test_case_no, filename, username, que_id):
    input_file = input_path + '/question{}'.format(que_id)
    input_f = open("{}/input{}.txt".format(input_file, test_case_no), "r")                       # standard input
    user_out_file = path_userCode + '/{}/question{}'.format(username, que_id)
    user_out_f = open('{}/output{}.txt'.format(user_out_file, test_case_no), "w+")                # user's output
    e_output_file = output_path + '/question{}/expected_output{}.txt'.format(que_id, test_case_no)
    e_output_f = open('{}'.format(e_output_file), 'r')                                       # expected/standard output

    result_value = config_sandbox(filename, input_f, user_out_f)   #
    input_f.close()
    user_out_f.close()

    same_output = False

    if result_value == 1:
        same_output = compare(user_out_f, e_output_f)            # False if different and True if same

    return same_output                                 # True if same else False


def main():
    filename = sys.argv[1].split(".")[0]      # FileName
    extension = sys.argv[1].split(".")[1]     # C or CPP or python
    username = sys.argv[2]                    # Username
    que_id = sys.argv[3]                      # Question ID

    return_value = compile(filename, extension)                          # calling compile()

    out_list = list()

    if return_value == 0:
        for i in range(0, NO_OF_QUESTIONS-1):
            run_code = run_test_cases(i+1, filename, username, que_id)  # calling runTestCases()
            out_list.append(1 if run_code else 0)

    total_file_path = path_userCode + '/{}/question{}'.format(username, que_id)
    total_file = open('{}/total_output.txt'.format(total_file_path), 'w+')

    for i in out_list:
        total_file.write("%d" % i)

    return 0


a = main()
