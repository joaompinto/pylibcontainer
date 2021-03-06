URL_MAP = {
    "alpine": "http://dl-cdn.alpinelinux.org/alpine/v3.9/releases/x86_64/alpine-minirootfs-3.9.4-x86_64.tar.gz",
    "ubuntu": "https://cloud-images.ubuntu.com/releases/19.04/release/ubuntu-19.04-server-cloudimg-amd64.tar.gz",
}


def get_url(key):
    return URL_MAP.get(key)
