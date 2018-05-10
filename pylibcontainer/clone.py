"""
    Launching namespaced processes
    References:
    - http://stackoverflow.com/questions/13373629/clone-process-support-in-python
    - http://crosbymichael.com/creating-containers-part-1.html
    - http://lxr.free-electrons.com/source/include/linux/sched.h?v=3.4
"""
from ctypes import (
    CDLL,
    c_void_p,
    c_int,
    c_char_p,
    cast,
    CFUNCTYPE,
)

import subprocess
import os
import sys

PARENT = "Parent"
CHILD = "Child"

CLONE_NEWPID = 0x20000000
CLONE_NEWNET = 0x40000000
CLONE_NEWUSER = 0x10000000
CLONE_NEWIPC = 0x08000000
CLONE_NEWUTS = 0x04000000
CLONE_NEWNS = 0x00020000

libc = CDLL("libc.so.6")

# We need the top of the stack.
stack = c_char_p(" " * 8096)
stack_top = c_void_p(cast(stack, c_void_p).value + 8096)


def namespaced_child_func():
    print "Child PID: %s" % os.getpid()

    if sys.argv[1:]:
        print subprocess.check_output(sys.argv[1:], shell=True)

    return 0

def app():
    f_c = CFUNCTYPE(c_int)(namespaced_child_func)

    flags = CLONE_NEWPID | CLONE_NEWNET | CLONE_NEWUSER \
    | CLONE_NEWIPC | CLONE_NEWUTS | CLONE_NEWNS

    libc.clone(f_c, stack_top, flags)

def run():
    print "Parent PID: %s" % os.getpid()

    app()

if __name__ == "__main__":
    run()
