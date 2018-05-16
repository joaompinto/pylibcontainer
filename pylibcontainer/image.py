from __future__ import print_function
import os
import shutil
import requests
import click
from tempfile import NamedTemporaryFile
from hashlib import sha256
from os.path import expanduser, join, exists, basename
from pylibcontainer.utils import eprint, HumanSize
from pylibcontainer.tar import extract_layer
from pylibcontainer import container
from clint.textui import progress


CACHE_PATH = join(expanduser("~"), ".pylibcontainer", "images_cache")


class Cache(object):
    cache_dir = CACHE_PATH

    """ Provides an image cahcing mechanism on disk """
    def __init__(self):
        if not exists(CACHE_PATH):
            os.makedirs(CACHE_PATH, 0o700)

    def get(self, cache_key, default=None):
        """ return info for cached file """
        cache_hash = sha256(cache_key).hexdigest()
        cache_fn = join(CACHE_PATH, "url_" + cache_hash)

        if exists(cache_fn):
            file_stat = os.stat(cache_fn)
            last_modified = file_stat.st_mtime
            file_size = file_stat.st_size
            return cache_fn, cache_hash, last_modified, file_size

        return default

    def put(self, filename, cache_key):
        """ put a file into cache """
        cache_hash = sha256(cache_key).hexdigest()
        cache_fn = join(CACHE_PATH, "url_" + cache_hash)
        shutil.move(filename, cache_fn)
        return cache_hash, cache_fn

def download(image_url):
    """ Download image (if not found in cache) and return it's filename """
    response = requests.head(image_url)
    if response.status_code != 200:
        eprint("http error code", response.status_code)
        exit(2)
    cache = Cache()
    cached_image = cache.get(image_url)
    if cached_image:
        cache_fn, cache_hash, last_modified, file_size = cached_image
        remote_file_size = int(response.headers.get('Content-Length'))
        remote_last_modified = response.headers.get('Last-Modified')
        if remote_file_size == file_size and remote_last_modified > last_modified:
            print("Using file from cache")
            return cache_hash, cache_fn
    file_size = int(response.headers.get('Content-Length', 0))
    print("Downloading image... {0} [{1:.2S}]".format(basename(image_url), HumanSize(file_size)))
    response = requests.get(image_url, stream=True)
    with NamedTemporaryFile(delete=False) as tmp_file:
        for chunk in progress.bar(response.iter_content(chunk_size=1024), expected_size=(file_size/1024) + 1):
            if chunk:
                tmp_file.write(chunk)
                tmp_file.flush()
    return cache.put(tmp_file.name, image_url)


@click.command()
@click.argument('image_url')
@click.argument('command', nargs=-1, type=click.Path())
def run(image_url, command):
    image_protocol = image_url.split(':')[0].lower()
    if image_protocol in ['http', 'https']:
        _, image_fn = download(image_url)
    else:
        _, image_fn = sha256(image_url).hexdigest(), image_url
    rootfs = extract_layer(image_fn)
    print("Executing %s" % ' '.join(command))
    container.runc(rootfs, command)
