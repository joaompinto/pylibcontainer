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

    pip install pylibcontainer

Configuration
-------------

Something here.

Usage
-----

Something else here.

Bugs and Feature Requests
-------------------------

Bug reports and feature requests are happily accepted via the `GitHub
Issue Tracker <https://github.com/joaompinto/pylibcontainer/issues>`__.
Pull requests are welcome. Issues that don't have an accompanying pull
request will be worked on as my time and priority allows.

Development
===========

To install for development:

1. Fork the
   `pylibcontainer <https://github.com/joaompinto/pylibcontainer>`__
   repository on GitHub
2. Create a new branch off of master in your fork.

Guidelines
----------

Testing
-------

Testing is done via `pytest <http://pytest.org/latest/>`__, driven by
`tox <http://tox.testrun.org/>`__.

-  testing is as simple as:

   -  ``pip install tox``
   -  ``tox``

-  If you want to pass additional arguments to pytest, add them to the
   tox command line after "--". i.e., for verbose pytext output on py27
   tests: ``tox -e py27 -- -v``

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
