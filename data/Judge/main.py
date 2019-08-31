import os
from sandbox import *
import sys

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


def probe(self):
    # add custom entries into the probe dict
    d = sandbox.probe(self, False)
    d['cpu'] = d['cpu_info'][0]
    d['mem'] = d['mem_info'][1]
    d['result'] = self.result
    return d


def compile(filename, username, extension, que_id):
    return_value = 1         # By default error while running file.
    if extension == 'c':
        return_value = os.system('gcc ' + '-o ' + '{}/{}/solution{} '.format(path_userCode, username, que_id) +
                                 path_userCode + '/{}/question{}/{}.c'.format(username, que_id, filename))

    elif extension == 'cpp':
        return_value = os.system('g++ ' + '-o ' + '{}/{}/solution{} '.format(path_userCode, username, que_id) +
                                 path_userCode + '/{}/question{}/{}.cpp'.format(username, que_id, filename))

    return return_value      # return 0 for success and 1 for


def run_test_cases(test_case_no, filename, extension, username, que_id, attempts):
    input_file = input_path + '/input{}.txt'.format(que_id)
    input_f = open("input_file", "r")
    code_file = path_userCode + '/{}/question{}/{}.{}'.format(username, que_id, filename, extension)
    code_f = open('output_file', os.O_RDWR)

    output_of_code = os.system('./{}/{}/solution{}'.format(path_userCode, username, que_id))


def main():
    filename = sys.argv[1]                    # FileName
    extension = sys.argv[1].split(".")        # C or CPP
    username = sys.argv[2]                    # Username
    que_id = sys.argv[3]                      # Question ID
    attempts = int(sys.argv[4])               # attempts

    return_value = compile(filename, username, extension, que_id)          # calling compile()

    if return_value == 0:
        for i in range(0, NO_OF_QUESTIONS-1):
            run_test_cases(i, filename, username, extension, que_id, attempts)           # calling runTestCases()
