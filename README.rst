pylibcontainer
==============

|pypi version| |GitHub Forks| |GitHub Open Issues| |travis-ci for master
branch| |coverage report for master branch| |sphinx documentation for
latest release|

Requirements
------------

-  Python 2.7 or 3.4+ (currently tested with 2.7, 3.4)

Installation
------------

.. code:: bash

    sudo pip install pylibcontainer

Examples
--------

.. code:: bash

    sudo pylibcontainer \
        run http://dl-cdn.alpinelinux.org/alpine/v3.7/releases/x86_64/alpine-minirootfs-3.7.0-x86_64.tar.gz

Bugs and Feature Requests
-------------------------

Bug reports and feature requests are happily accepted via the `GitHub
Issue Tracker <https://github.com/joaompinto/pylibcontainer/issues>`__.
Pull requests are welcome. Issues that don't have an accompanying pull
request will be worked on as my time and priority allows.

Guidelines
----------

Testing
-------

Testing is done via `pytest <http://pytest.org/latest/>`__, driven by
`tox <http://tox.testrun.org/>`__.

Testing is as simple as:

.. code:: bash

    sudo pip install tox
    tox

Release Checklist
-----------------

.. |pypi version| image:: https://img.shields.io/pypi/v/pylibcontainer.svg?maxAge=2592000
   :target: https://pypi.python.org/pypi/pylibcontainer
.. |GitHub Forks| image:: https://img.shields.io/github/forks/joaompinto/pylibcontainer.svg
   :target: https://github.com/joaompinto/pylibcontainer/network
.. |GitHub Open Issues| image:: https://img.shields.io/github/issues/joaompinto/pylibcontainer.svg
   :target: https://github.com/joaompinto/pylibcontainer/issues
.. |travis-ci for master branch| image:: https://secure.travis-ci.org/joaompinto/pylibcontainer.png?branch=master
   :target: http://travis-ci.org/joaompinto/pylibcontainer
.. |coverage report for master branch| image:: https://codecov.io/github/joaompinto/pylibcontainer/coverage.svg?branch=master
   :target: https://codecov.io/github/joaompinto/pylibcontainer?branch=master
.. |sphinx documentation for latest release| image:: https://readthedocs.org/projects/pylibcontainer/badge/?version=latest
   :target: https://readthedocs.org/projects/pylibcontainer/?badge=latest
