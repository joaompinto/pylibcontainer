
URL_MAP = {
    'alpine':
    'http://dl-cdn.alpinelinux.org/alpine/v3.8/releases/x86_64/alpine-minirootfs-3.8.2-x86_64.tar.gz',
    'ubuntu':
    'https://cloud-images.ubuntu.com/releases/18.10/release/ubuntu-18.10-server-cloudimg-amd64.tar.gz'
}


def get_url(key):
    return URL_MAP.get(key)
