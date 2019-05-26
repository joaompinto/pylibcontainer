from __future__ import print_function
import os
import shutil
import hashlib
import requests
import click
from tempfile import NamedTemporaryFile
from hashlib import sha256
from os.path import expanduser, join, exists, basename
from .utils import HumanSize
from .tar import extract_layer
from . import trust
from . import container
from .colorhelper import print_info, print_error, print_warn, print_success
from .colorhelper import success
from .image_index import get_url
from clint.textui import progress
from dateutil.parser import parse as parsedate
from datetime import datetime

CACHE_PATH = join(expanduser("~"), ".pylibcontainer", "images_cache")


class Cache(object):
    cache_dir = CACHE_PATH

    """ Provides an image caching mechanism on disk """

    def __init__(self):
        if not exists(CACHE_PATH):
            os.makedirs(CACHE_PATH, 0o700)

    def get(self, cache_key, default=None):
        """ return info for cached file """
        cache_hash = sha256(cache_key.encode()).hexdigest()
        cache_fn = join(CACHE_PATH, "url_" + cache_hash)

        if exists(cache_fn):
            file_stat = os.stat(cache_fn)
            last_modified = datetime.fromtimestamp(file_stat.st_mtime)
            file_size = file_stat.st_size
            return cache_fn, cache_hash, last_modified, file_size

        return default

    def put(self, filename, cache_key):
        """ put a file into cache """
        cache_hash = sha256(cache_key.encode()).hexdigest()
        cache_fn = join(CACHE_PATH, "url_" + cache_hash)
        shutil.move(filename, cache_fn)
        return cache_hash, cache_fn


def download(image_url):
    """ Download image (if not found in cache) and return it's filename """

    response = requests.head(image_url)
    file_size = remote_file_size = int(response.headers.get("Content-Length"))
    remote_last_modified = parsedate(response.headers.get("Last-Modified")).replace(
        tzinfo=None
    )
    remote_is_valid = response.status_code == 200 and file_size and remote_last_modified

    # Check if image is on cache
    cache = Cache()
    cached_image = cache.get(image_url)
    if cached_image:
        if remote_is_valid:
            cache_fn, cache_hash, last_modified, file_size = cached_image
            if remote_file_size == file_size and remote_last_modified < last_modified:
                print_info("Using file from cache", CACHE_PATH)
                return cache_hash, cache_fn
            print_info("Downloading new remote file because an update was found")
        else:
            print_warn("Unable to check the status for " + image_url)
            print_warn("Assuming local cache is valid")

    # Not cached, and no valid remote information was found
    if not remote_is_valid:
        print_error(
            "Unable to get file, http_code=%s, size=%s, last_modified=%s"
            % (response.status_code, remote_file_size, remote_last_modified)
        )
        exit(2)

    # Dowload image
    print_info(
        "Downloading image... ",
        "{0} [{1:.2S}]".format(basename(image_url), HumanSize(file_size)),
    )
    remote_sha256 = hashlib.sha256()
    response = requests.get(image_url, stream=True)
    with NamedTemporaryFile(delete=False) as tmp_file:
        for chunk in progress.bar(
            response.iter_content(chunk_size=1024), expected_size=(file_size / 1024) + 1
        ):
            if chunk:
                remote_sha256.update(chunk)
                tmp_file.write(chunk)
                tmp_file.flush()

    # Verify image integrity
    trust_verify = trust.verify(image_url, tmp_file.name, remote_sha256.hexdigest())
    if not trust_verify or not trust_verify.valid or not trust_verify.username:
        print_error("Integrity/authenticity error - GPG signature mismatch!")
        exit(3)
    print("{0:>10}: {1}".format("GPG Signer", success(trust_verify.username)))
    print("{0:>10}: {1}".format("GPG ID", success(trust_verify.pubkey_fingerprint)))
    print("{0:>10}: {1}".format("Creation", success(trust_verify.creation_date)))

    return cache.put(tmp_file.name, image_url)


@click.command()
@click.argument("image_url")
@click.option("--as_root", is_flag=True)
@click.option("--overlay", "-o", multiple=True)
@click.argument("command", nargs=-1)
def run(image_url, command, as_root, overlay):
    url = get_url(image_url)
    image_url = url or image_url
    if not image_url:
        print_info("No index was found for image", image_url)
        exit(5)
    is_validate_only = False
    if not command:
        command = ["/bin/sh"]
    image_protocol = image_url.split(":")[0].lower()
    if image_protocol in ["http", "https"]:
        _, image_fn = download(image_url)
    else:
        _, image_fn = sha256(image_url).hexdigest(), image_url
    rootfs = extract_layer(image_fn)
    if len(command) == 1 and command[0] == "-":
        is_validate_only = True
        print("Validating container setup with the rootfs")
    else:
        print_info("Executing", " ".join(command))
    _, exit_code = container.runc(rootfs, command, as_root, overlay)
    if exit_code != 0:
        print_error("Last command returned an error")
    elif is_validate_only:
        print_success("OK")
