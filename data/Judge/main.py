import os
import sandbox
import sys

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


def configSandbox(args, inputFile, outFile):
    # sandbox configuration
    cookbook = {
        'args': args[1:],               # targeted program
        'stdin': inputFile,             # input to targeted program
        'stdout': outFile,              # output from targeted program
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

def compare():


def compile():
    #compilation

def runtestcases():
    #runTestCases

def main():
    # main.py is called from views.py by command

    #os.system('python main.py '+ '{}/{}/question{}/code{}-{}.cpp'.format(path1, username, qn, qn, attempts) + ' '+
    #          username + ' ' + qn + ' ' + attempts)

    filename = sys.argv[1]                    # FileName
    extension = sys.argv[1].split(".")    # C or CPP
    username = sys.argv[2]                    # Username
    queID = sys.argv[3]                       # Question ID



    # Configuration of Sandbox
    # calling configSandbox()
    # calling compile()
    # calling runTestCases()
    # calling compare()



