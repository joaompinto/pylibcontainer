URL_MAP = {
    "alpine": "https://dl-cdn.alpinelinux.org/alpine/v3.17/releases/x86_64/alpine-minirootfs-3.17.2-x86_64.tar.gz",
    "ubuntu": "https://cloud-images.ubuntu.com/releases/19.04/release/ubuntu-19.04-server-cloudimg-amd64.tar.gz",
}


def get_url(key):
    return URL_MAP.get(key)
