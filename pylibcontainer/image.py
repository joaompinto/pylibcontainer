from __future__ import print_function
import os
import re
import shutil
import hashlib
import requests
import click
from tempfile import NamedTemporaryFile
from hashlib import sha256
from os.path import expanduser, join, exists, basename, dirname, realpath
from pylibcontainer.utils import HumanSize
from pylibcontainer.tar import extract_layer
from pylibcontainer import container
from pylibcontainer.colorhelper import print_info, print_error, print_warn, print_success
from pylibcontainer.colorhelper import success, error
from clint.textui import progress
from gnupg import GPG


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

def get_sha256sum(download_url):
    """ Try to obtain the sha256 for the file provided at the url """
    # Support Alpine/Ubuntu Linux schemes as described at:
    #   https://github.com/joaompinto/pylibcontainer/issues/1
    possible_gpg_path = (download_url+".sha256", dirname(download_url)+"/SHA256SUMS")
    file_name = basename(download_url)
    for url in possible_gpg_path:
        response = requests.get(url)
        if response.status_code == 200:
            sha256_sum = re.findall(r'^(\S+).*' + file_name, response.content)
            if sha256_sum:
                return url, sha256_sum[0], response.content

    return None, None, None

def gpg_verify(chksum_url, chksum_data):
    """ Perform GPG validation """
    print(chksum_data)
    gpg_url = chksum_url.rsplit(".", 1)[0]+".gpg"
    asc_url = chksum_url.rsplit(".", 1)[0]+".asc"
    possible_paths = (gpg_url, asc_url)
    gpg_sig_data = None
    for url in possible_paths:
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            gpg_sig_data = response.content
            break
    if gpg_sig_data is None:
        return None
    print("GPG validation")
    gpg_keyring_fn = join(realpath(dirname(__file__)), 'trusted', 'keys.gpg')
    assert exists(gpg_keyring_fn)
    gpg = GPG(keyring=gpg_keyring_fn, verbose=True)
    print(gpg_sig_data)
    with NamedTemporaryFile(delete=False) as gpg_sig_file:
        print(gpg_sig_file.name)
        gpg_sig_file.write(gpg_sig_data)
        verified = gpg.verify_data(gpg_sig_file.name, chksum_data)
    print(verified.trust_level)
    return None

def download(image_url):
    """ Download image (if not found in cache) and return it's filename """
    response = requests.head(image_url)
    file_size = remote_file_size = int(response.headers.get('Content-Length'))
    remote_last_modified = response.headers.get('Last-Modified')
    remote_is_valid = response.status_code == 200 and file_size and remote_last_modified

    # Check if image is on cache
    cache = Cache()
    cached_image = cache.get(image_url)
    if cached_image:
        if remote_is_valid:
            cache_fn, cache_hash, last_modified, file_size = cached_image
            if remote_file_size == file_size and remote_last_modified > last_modified:
                print_info("Using file from cache", CACHE_PATH)
                return cache_hash, cache_fn
            print_info("Downloading new remote file because an update was found")
        else:
            print_warn("Unable to check the status for "+ image_url)
            print_warn("Assuming local cache is valid")

    # Not cached, and no valid remote information was found
    if not remote_is_valid:
        print_error(
            "Unable to get file, http_code=%s, size=%s, last_modified=%s" %
            (response.status_code, remote_file_size, remote_last_modified)
        )
        exit(2)

    # Not cached, valid remote info, attempt to download
    # But first try to locate the SHA256 cheksum
    sha256url, sha256sum, sha256data = get_sha256sum(image_url)
    if not sha256sum:
        print_error("Unable to validate rootfs integrity because no SHA256 checksum found")
        exit(3)
    gpg_status = gpg_verify(sha256url, sha256data)
    if gpg_status is None:
        print_error("Unable to validate authenticity, no .gpg file was found ")
        exit(4)

    print("Downloading image... {0} [{1:.2S}]".format(basename(image_url), HumanSize(file_size)))
    remote_sha256 = hashlib.sha256()
    response = requests.get(image_url, stream=True)
    with NamedTemporaryFile(delete=False) as tmp_file:
        for chunk in progress.bar(response.iter_content(chunk_size=1024), expected_size=(file_size/1024) + 1):
            if chunk:
                remote_sha256.update(chunk)
                tmp_file.write(chunk)
                tmp_file.flush()
    if remote_sha256.hexdigest() == sha256sum:
        print("SHA256 Integrity - " + success("OK"))
    else:
        print("SHA256 Integrity - " + error("MISMATCH"))
        exit(3)

    return cache.put(tmp_file.name, image_url)


@click.command()
@click.argument('image_url')
@click.argument('command', nargs=-1)
def run(image_url, command):
    is_validate_only = False
    if not command:
        command = ['/bin/sh']
    image_protocol = image_url.split(':')[0].lower()
    if image_protocol in ['http', 'https']:
        _, image_fn = download(image_url)
    else:
        _, image_fn = sha256(image_url).hexdigest(), image_url
    rootfs = extract_layer(image_fn)
    if len(command) == 1 and command[0] == "-":
        is_validate_only = True
        print("Validating container setup with the rootfs")
    else:
        print_info("Executing", ' '.join(command))
    _, exit_code = container.runc(rootfs, command)
    if exit_code != 0:
        print_error("An error was detected")
    elif is_validate_only:
        print_success("OK")
