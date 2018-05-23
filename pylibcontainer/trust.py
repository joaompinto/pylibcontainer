"""
    This module provides the image integrity/authenticity verification features.

    The following schemes are suppported:

    a) A download_url.asc file is found, on this case intregrity & authentication
    will be performed in a single setup, with gpg verify of the download content vs .asc

    b) A dirname(download_url)/{SHA256SUMS|SHA256SUMS.gpg} are found which will need:
        1. Verify that SHA256SUMS.gpg provides a valid signature for SHA256SUMS
        2. Verify that the downloaded file SHA256SUM matches the corresponding line in SHA256SUMS
"""
import requests
import re
from gnupg import GPG
from StringIO import StringIO
from os.path import join, dirname, realpath, basename
from tempfile import NamedTemporaryFile

def gpg_verify(gpg_signature, filename):
    """ Verify that the signature is valid for the content of the filename """
    gpg_sign_stream = StringIO(gpg_signature)
    gpg_keyring_fn = join(realpath(dirname(__file__)), 'trusted', 'keyring.gpg')
    gpg = GPG(keyring=gpg_keyring_fn)
    return gpg.verify_file(gpg_sign_stream, filename)


def verify(download_url, local_filename, sha256sum):
    """ Verify integrity/authenticity a file """

    # If detached signatured is found, use method a)
    for ext in ['.asc', '.sig']:
        asc_url = download_url+ext
        response = requests.get(asc_url)
        if response.status_code == 200:
            return gpg_verify(response.content, local_filename)

    # If SHA256SUMS is found, follow scheme b)
    sha256sum_url = dirname(download_url)+"/SHA256SUMS"
    response = requests.get(sha256sum_url)
    if response.status_code == 200:
        sha256sum_content = response.content
        file_name = basename(download_url)

        # Search if the download filename is found in the SHA256SUMS list
        # and the checksums matche
        remote_sha256sum = re.findall(r'^(\S+).*' + file_name, sha256sum_content)
        if remote_sha256sum:
            remote_sha256sum = remote_sha256sum[0]
        if remote_sha256sum != sha256sum:
            return None

        # Verify if the remote_sha256sum is trusted
        sha256sum_gpg_url = dirname(download_url)+"/SHA256SUMS.gpg"
        response = requests.get(sha256sum_gpg_url)
        if response.status_code == 200:
            with NamedTemporaryFile(delete=False) as tmp_sha256sum_file:
                tmp_sha256sum_file.write(sha256sum_content)
                tmp_sha256sum_file.flush()
                return gpg_verify(response.content, tmp_sha256sum_file.name)

    return None
