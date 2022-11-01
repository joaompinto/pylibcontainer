from __future__ import print_function

import tarfile
from os.path import join, exists, basename
from os import makedirs
from tempfile import gettempdir, mkdtemp
from shutil import move
from pylibcontainer.colorhelper import print_info


def extract_layer(layer_fn):
    cache_key = basename(layer_fn)
    cache_prefix = join(gettempdir(), "pylibcontainer", "layer.cache")
    cache_path = join(cache_prefix, cache_key)
    if not exists(cache_prefix):
        makedirs(cache_prefix, 0o700)

    # Image is not yet cached, save and extract it
    if not exists(cache_path):
        print_info("Mounting read-only rootfs at", cache_path)
        tarfile.os.mknod = (
            lambda x, y, z: 0
        )  # Monkey patch mknod because some layers include devices
        with tarfile.open(layer_fn) as image_tar:
            tmp_dir = mkdtemp()
            
            import os
            
            def is_within_directory(directory, target):
                
                abs_directory = os.path.abspath(directory)
                abs_target = os.path.abspath(target)
            
                prefix = os.path.commonprefix([abs_directory, abs_target])
                
                return prefix == abs_directory
            
            def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
            
                for member in tar.getmembers():
                    member_path = os.path.join(path, member.name)
                    if not is_within_directory(path, member_path):
                        raise Exception("Attempted Path Traversal in Tar File")
            
                tar.extractall(path, members, numeric_owner=numeric_owner) 
                
            
            safe_extract(image_tar, tmp_dir)
        move(tmp_dir, cache_path)
    else:
        print_info("Mounting (cached) read-only rootfs at", cache_path)

    return cache_path
