#/bin/sh
KEYRING=pylibcontainer/trusted/keyring.gpg
GPG="gpg --no-default-keyring --keyring $KEYRING"
rm -f $KEYRING
$GPG --fingerprint

# Alpine Linux Key
curl https://alpinelinux.org/keys/ncopa.asc | $GPG --import -

# Ubuntu Linux Cloud Image Keys
$GPG --keyserver hkp://keyserver.ubuntu.com --recv-keys 0x7DB87C81

# Arch Linux

curl https://pgp.mit.edu/pks/lookup?op=get&fingerprint=on&search=0x3348882F6AC6A4C2 | $GPG --import -
