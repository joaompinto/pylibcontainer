
URL_MAP = {
    'alpine':
    'http://dl-cdn.alpinelinux.org/alpine/v3.7/releases/x86_64/alpine-minirootfs-3.7.0-x86_64.tar.gz',
    'ubuntu':
    'https://cloud-images.ubuntu.com/artful/current/artful-server-cloudimg-amd64.tar.gz'
}


def get_url(key):
    return URL_MAP.get(key)