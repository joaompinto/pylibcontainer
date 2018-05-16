from __future__ import print_function

import tarfile
from os.path import join, exists, basename
from os import makedirs
from tempfile import gettempdir, mkdtemp
from shutil import move

def extract_layer(layer_fn):
    cache_key = basename(layer_fn)
    cache_prefix = join(gettempdir(), "ctinspector", "layer.cache")
    cache_path = join(cache_prefix, cache_key)
    if not exists(cache_prefix):
        makedirs(cache_prefix, 0o700)

    # Image is not yet cached, save and extract it
    if not exists(cache_path):
        tarfile.os.mknod = lambda x, y, z: 0  # Monkey patch mknod because some layers include devices
        with tarfile.open(layer_fn) as image_tar:
            tmp_dir = mkdtemp()
            image_tar.extractall(tmp_dir)
        move(tmp_dir, cache_path)
    else:
        print("Using rootfs dir from tmp cache")

    return cache_path
