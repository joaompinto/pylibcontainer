import os
import pwd
import grp
from uuid import uuid4
from os.path import exists, join

from pyroute2 import netns
from tmsyscall.unshare import unshare, setns
from tmsyscall.unshare import (
    CLONE_NEWNS,
    CLONE_NEWUTS,
    CLONE_NEWIPC,
    CLONE_NEWPID,
    CLONE_NEWNET,
)
from tmsyscall.mount import (
    MS_BIND,
    MS_PRIVATE,
    MS_REC,
    MNT_DETACH,
    MS_REMOUNT,
    MS_RDONLY,
)
from tmsyscall.mount import mount, unmount, mount_procfs
from tmsyscall.pivot_root import pivot_root
from pylibcontainer.utils import HumanSize
from pylibcontainer.colorhelper import print_info, print_list
from pylibcontainer.network import set_loopback, set_container_veth, set_host_veth

DEFAULT_limit_in_bytes = 1024 * 1024
NETNS_DIR = "/var/run/netns/"


def drop_privileges(uid_name="nobody", gid_name="nogroup"):
    """ Switch from root to an uid/gid """

    # Get the uid/gid from the name
    running_uid = pwd.getpwnam(uid_name).pw_uid
    running_gid = grp.getgrnam(gid_name).gr_gid

    # Remove group privileges
    os.setgroups([])

    # Try setting the new uid/gid
    os.setgid(running_gid)
    os.setuid(running_uid)

    # Ensure a very conservative umask
    _ = os.umask(0o77)


def setup_process_isolation(rootfs_path, overlay_path):
    # Detach from parent's mount, hostname, ipc and net  namespaces
    unshare(CLONE_NEWNS | CLONE_NEWUTS | CLONE_NEWIPC | CLONE_NEWNET)

    # Set mount propagation to private recursively. Hopefully equivalent to
    #    mount --make-rprivate /
    # This is needed to prevent mounts in this container leaking to the parent.
    mount("none", "/", None, MS_REC | MS_PRIVATE, "")

    # chmod / 755 for unprivileged user access
    os.chmod(rootfs_path, 0o755)

    # This bind mount call is needed to satisfy a requirement of the `pivotroot` system call
    #   "new_root and put_old must not be on the same file system as the current root"
    # It is achieved by mounting "new_root" as a bind mount to "new root"
    mount(rootfs_path, rootfs_path, "", MS_BIND | MS_REC, "")

    old_root = join(rootfs_path, ".old_root")
    if not exists(old_root):
        os.makedirs(old_root, 0o700)

    # Remount it as read-only
    mount(rootfs_path, rootfs_path, "", MS_BIND | MS_REC | MS_REMOUNT | MS_RDONLY, "")
    pivot_root(rootfs_path, old_root)

    # We don't want the host root to be available to the container
    unmount("/.old_root", MNT_DETACH)

    os.chdir("/")

    # Mount /proc for apps that need it
    if not exists("proc"):
        os.makedirs("proc", 0o700)
    mount_procfs(".")  # py


def child(rootfs_path, cmd, container_id, as_root, overlay):
    newns = os.open(NETNS_DIR + container_id, os.O_RDONLY)
    setup_process_isolation(rootfs_path, overlay)
    setns(newns, 0)
    set_container_veth()
    set_loopback()
    if not as_root:
        drop_privileges()
    if len(cmd) > 1 or cmd[0] != "-":
        os.execvp(cmd[0], cmd)
    os.close(newns)


def parent(child_pid):
    container_id = str(uuid4())
    result = os.waitpid(child_pid, 0)
    return result


def runc(rootfs_path, command, as_root, overlay):
    container_id = str(uuid4())
    netns.create(container_id)
    set_host_veth(container_id)
    # Detach from pid namespace so that our child get's a clean /proc with the new namespace
    unshare(CLONE_NEWPID)
    pid = os.fork()
    if pid == 0:
        child(rootfs_path, command, container_id, as_root, overlay)
        exit(0)
    return parent(pid)
