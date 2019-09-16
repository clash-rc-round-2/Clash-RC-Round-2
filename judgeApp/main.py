import resource
import subprocess
import os


def setlimits():
    resource.setrlimit(resource.RLIMIT_CPU, (1, 1))
    resource.setrlimit(resource.RLIMIT_AS, (268435456, 268435456))
    # resource.setrlimit(resource.RLIMIT_STACK, (1310720, 1310720))


def run_in_sandbox(exec_path, lang, ipf, opf, errf):
    if lang == 'py':
        child = subprocess.Popen(
            ['python3', exec_path], preexec_fn=setlimits, stdin=ipf, stdout=opf, stderr=errf)
    else:
        child = subprocess.Popen(
            ['./' + exec_path], preexec_fn=setlimits, stdin=ipf, stdout=opf, stderr=errf, shell=True)

    child.wait()
    return child.returncode
