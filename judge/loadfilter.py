from seccomp import *

# create a filter object with a default KILL action


def install_filter():
    f = SyscallFilter(defaction=KILL)
    f.add_rule(ALLOW, "read", Arg(0, EQ, 0))
    f.add_rule(ALLOW, "write", Arg(0, EQ, 1))
    f.add_rule(ALLOW, "write", Arg(0, EQ, 2))
    f.add_rule(ALLOW, "fstat")
    f.add_rule(ALLOW, 'ioctl')
    f.add_rule(ALLOW, 'sigaltstack')
    f.add_rule(ALLOW, "rt_sigaction")
    f.add_rule(ALLOW, "exit_group")
    f.load()