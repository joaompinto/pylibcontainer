
# You can test it using:
#   wget https://partner-images.canonical.com/core/artful/current/ubuntu-artful-core-cloudimg-amd64-root.tar.gz
#   sudo bash -c "mkdir rootfs; tar xvf ubuntu-artful-core-cloudimg-amd64-root.tar.gz -C rootfs"
#   sudo python example2.py bash

from __future__ import print_function
import subprocess
import os
import sys
from tmsyscall.unshare import unshare, CLONE_NEWNS, CLONE_NEWUTS, CLONE_NEWIPC, CLONE_NEWPID, CLONE_NEWNET
from tmsyscall.mount import mount, unmount, MS_BIND, MS_PRIVATE, MS_REC, MNT_DETACH
from tmsyscall.mount import mount_procfs
from tmsyscall.pivot_root import pivot_root
from os.path import exists


def setup_process_isolation():
    # Detach from parent's mount, hostname, ipc and net  namespaces
    unshare(CLONE_NEWNS| CLONE_NEWUTS | CLONE_NEWIPC| CLONE_NEWNET)

    # Set mount propagation to private recursively. Hopefully equivalent to
    #    mount --make-rprivate /
    # This is needed to prevent mounts in this container leaking to the parent.
    mount('none', '/', None, MS_REC|MS_PRIVATE, "")

    # The bind mount call is needed to satisfy a requirement of the `pivotroot` command
    # the OS requires that `pivotroot` be used to swap two filesystems that are not part of the same tree
    mount("rootfs", "rootfs", "", MS_BIND|MS_REC, "")
    if not exists("rootfs/.old_root"):
        os.makedirs("rootfs/.old_root", 0o700)
    pivot_root("rootfs", "rootfs/.old_root")
    os.chdir("/")

    # We don't want the host root to be available to the container
    unmount("/.old_root", MNT_DETACH)
    os.rmdir(".old_root")

    # Mount /proc for apps that need it
    if not exists("proc"):
        os.makedirs("proc", 0o700)
    mount_procfs('.')

def child():
    setup_process_isolation()
    proc = subprocess.Popen(sys.argv[1:], stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    proc.communicate()


def parent(child_pid):
    pid, status = os.waitpid(child_pid, 0)
    print("wait returned, pid = %d, status = %d" % (pid, status))


def main():
    # Detach from pid namespace so that our child get's a clean /proc with the new namespace
    unshare(CLONE_NEWPID)
    pid = os.fork()
    if pid == 0:
        child()
    else:
        parent(pid)

main()
