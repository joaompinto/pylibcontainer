pylibcontainer
==============

This package provides an [OCI runtime specification](https://github.com/opencontainers/runtime-spec) implementation library written in Python.

[![pypi version](https://img.shields.io/pypi/v/pylibcontainer.svg?maxAge=2592000)](https://pypi.python.org/pypi/pylibcontainer)
[![GitHub Forks](https://img.shields.io/github/forks/joaompinto/pylibcontainer.svg)](https://github.com/joaompinto/pylibcontainer/network)
[![GitHub Open Issues](https://img.shields.io/github/issues/joaompinto/pylibcontainer.svg)](https://github.com/joaompinto/pylibcontainer/issues)
[![travis-ci for master branch](https://secure.travis-ci.org/joaompinto/pylibcontainer.png?branch=master)](http://travis-ci.org/joaompinto/pylibcontainer)
[![coverage report for master branch](https://codecov.io/github/joaompinto/pylibcontainer/coverage.svg?branch=master)](https://codecov.io/github/joaompinto/pylibcontainer?branch=master)
[![sphinx documentation for latest release](https://readthedocs.org/projects/pylibcontainer/badge/?version=latest)](https://readthedocs.org/projects/pylibcontainer/?badge=latest)


Status
------
pylibcontainer it's in a verly early stage of development.

Feature list:
- [X] - Download and validate rootfs distro tarballs 
- Unshare from parent namespace
    * [X] Filesystem mounts
    * [X] Network
    * [X] IPC
    * [X] Process information
    * [ ] Usernames mapping
- [ ] Writable overlay mount points
- [ ] Network



Requirements
------------

- Python 3.7+ (currently tested with 3.7)

Installation
------------

```bash
sudo pip install https://github.com/joaompinto/pylibcontainer/archive/master.zip
```

Examples
--------

```bash
sudo pylibcontainer run alpine
```

Bugs and Feature Requests
-------------------------

Bug reports and feature requests are happily accepted via the [GitHub
Issue
Tracker](https://github.com/joaompinto/pylibcontainer/issues).
Pull requests are welcome. Issues that don't have an accompanying pull
request will be worked on as my time and priority allows.

Guidelines
----------

Testing
-------

Testing is done via [pytest](http://pytest.org/latest/), driven by
[tox](http://tox.testrun.org/).

Testing is as simple as:

```bash
sudo pip install tox
tox
```

Release Checklist
-----------------
