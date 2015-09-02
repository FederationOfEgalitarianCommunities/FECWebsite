.. _How to Get Started:

Getting Started
================

This section covers setting up a dev machine to work on the website's source
code.


Grab the Source
----------------

Use ``git`` to clone the current source code repository:

.. code-block:: bash

    $ git clone http://bugs.sleepanarchy.com/fec.git

Switch over to the ``develop`` branch, where new development occurs. Only
completed versions should be merged directly into the ``master`` branch.


Install Prerequisites
----------------------

You should install `python 2`_ and `pip`_ via your package manager.

On Arch Linux:

.. code-block:: bash

    $ sudo pacman -S python2 python2-pip

On Slackware:

.. code-block:: bash

    $ sudo /usr/sbin/slackpkg install python
    $ wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
    $ sudo python get-pip.py

On Debian/Ubuntu:

.. code-block:: bash

    $ sudo apt-get install python-pip

Optionally you may want to install `virtualenv`_ and `virtualenvwrapper`_ to
manage and isolate the python dependencies.

.. code-block:: bash

    $ sudo pip install virtualenv virtualenvwrapper

Make sure to do the initial setup for `virtualenv`_:

.. code-block:: bash

    $ export WORKON_HOME=~/.virtualenv/
    $ mkdir -p $WORKON_HOME
    $ source virtualenvwrapper.sh

Then you may create an environment for the FEC dependenies:

.. code-block:: bash

    $ mkvirtualenv FEC

You may then install dependencies into this virtual environment. There are
multiple tiers of dependencies:

* ``base`` - minimum requirements needed to run the application
* ``test`` - requirements necessary for running the test suite
* ``local`` - development prerequisites such as the debug toolbar and
  documentation builders
* ``production`` - all packages required for real world usage

A set of dependencies may be installed via `pip`_:

.. code-block:: bash

    $ workon FEC
    $ pip install -r requirements/local.txt


Configuration
--------------

Some settings are set through environmental variables instead of files. These
include settings with sensitive information, and allows us to keep the
information out of version control.

You may set these variables directly in the terminal or add them to your
virtualenv's ``activate`` script::

    $ DB_USER='prikhi' DB_NAME='FEC' ./manage.py <command>
    $ export DB_NAME='FEC'
    $ ./manage.py <command>

The required environmental variables are ``DJANGO_SECRET_KEY``, ``DB_NAME`` and
``DB_USER``.


Create the Database
--------------------

Create the initial database by running ``createdb``:

.. code-block:: bash

    $ export DJANGO_SETTINGS_MODULE=core.settings.local
    $ cd fec
    $ ./manage.py createdb


Running
--------

You should now be able to run the server:

.. code-block:: bash

    $ ./manage.py runserver

You can visit ``http://localhost:8000/`` in a web browser to check the site
out.


Testing
--------

After making changes, run the test suite with ``py.test``:

.. code-block:: bash

    $ cd fec
    $ py.test

Every test should pass before you commit your changes.


.. _pip: http://www.pip-installer.org/en/latest/

.. _python 2: http://www.python.org/

.. _virtualenv: https://github.com/pypa/virtualenv

.. _virtualenvwrapper: https://github.com/bernardofire/virtualenvwrapper
