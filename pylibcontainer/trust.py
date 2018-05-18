"""
    This module provides the image integrity/authenticity verification features.

    The following schemes are suppported:

    a) An download_url.asc file is provided, on this case intregrity & authentication
    will be performed in a single setup, with gpg verify of the download content vs .asc

    b) A dirname(download_url)/{SHA256SUMS|SHA256SUMS.gpg} are found which will need:
        1. Verify that SHA256SUMS.gpg provides a valid signature for SHA256SUMS
        2. Verify that the content SHA256SUM matches the corresponding line in SHA256SUMS
"""
from gnupg import GPG
