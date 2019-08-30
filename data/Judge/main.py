import os
import sandbox
import sys

NO_OF_QUESTIONS = 6

# paths
path = os.getcwd()    # 'clash'
path_userCode = path + '/data/usersCode'
input_path = path +  '/data/standard/input'
output_path = path +  '/data/standard/output'


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


def config_sandbox(args, input_file, out_file):
    # sandbox configuration
    cookbook = {
        'args': args[1:],               # targeted program
        'stdin': input_file,             # input to targeted program
        'stdout': out_file,              # output from targeted program
        'stderr': sys.stderr,           # error from targeted program
        'quota': dict(wallclock=30000,  # 30 sec
                      cpu=2000,         # 2 sec
                      memory=8388608,   # 8 MB
                      disk=1048576)}    # 1 MB
    # create a sandbox instance and execute till end
    msb = sandbox.Sandbox(**cookbook)
    msb.run()
    # verbose statistics
    sys.stderr.write("result: %(result)s\ncpu: %(cpu)dms\nmem: %(mem)dkB\n" %
        msb.probe())
    return os.EX_OK


def compile(filename, username, extension, que_id):
    return_value = 1         # By default error while running file.
    if extension == 'c':
        return_value = os.system('gcc ' + '-o ' + '{}/{}/solution{} '.format(path_userCode, username, que_id) +
                                 filename)

    elif extension == 'cpp':
        return_value = os.system('g++ ' + '-o ' + '{}/{}/solution{} '.format(path_userCode, username, que_id) +
                                 filename)

    return return_value      # return 0 for success and 1 for


def run_test_cases(filename, username, que_id, attempts):


def main():
    # main.py is called from views.py by command
    # os.system('python main.py '+ '{}/{}/question{}/code{}-{}.cpp'.format(path1, username, qn, qn, attempts) + ' '+
    #          username + ' ' + qn + ' ' + attempts)

    filename = sys.argv[1]                    # FileName
    extension = sys.argv[1].split(".")        # C or CPP
    username = sys.argv[2]                    # Username
    que_id = sys.argv[3]                      # Question ID
    attempts = int(sys.argv[4])               # attempts

    return_value = compile(filename, username, extension, que_id)          # calling compile()

    if return_value==0:
        for i in range(0, NO_OF_QUESTIONS-1):
            run_test_cases(filename, username, que_id, attempts)           # calling runTestCases()