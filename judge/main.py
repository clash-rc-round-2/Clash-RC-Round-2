import resource
import subprocess


def setlimits():
    resource.setrlimit(resource.RLIMIT_CPU, (6, 6))
    resource.setrlimit(resource.RLIMIT_AS, (33554432, 33554432))
    resource.setrlimit(resource.RLIMIT_STACK, (1310720, 1310720))


child = subprocess.Popen(['python3', 'target.py'], preexec_fn=setlimits)

child.wait()
print('returncode', child.returncode)
