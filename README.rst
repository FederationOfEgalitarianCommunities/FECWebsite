Federation of Egalitarian Communities Website
==============================================

This is the Mezzanine project that powers http://thefec.org.

Open issues live at http://bugs.sleepanarchy.com/projects/fec/issues

The project roadmap lives at http://bugs.sleepanarchy.com/projects/fec/roadmap

.. image:: https://travis-ci.org/FederationOfEgalitarianCommunities/FECWebsite.svg?branch=develop
    :target: https://travis-ci.org/FederationOfEgalitarianCommunities/FECWebsite
    :alt: Test Status

.. image:: https://coveralls.io/repos/FederationOfEgalitarianCommunities/FECWebsite/badge.svg?branch=develop
    :target: https://coveralls.io/r/FederationOfEgalitarianCommunities/FECWebsite?branch=develop
    :alt: Code Coverage Status


.. image:: https://readthedocs.org/projects/fecwebsite/badge/?version=latest
    :target: https://readthedocs.org/projects/fecwebsite/?badge=latest
    :alt: Documentation Status


Quickstart
-----------

Clone source code::

    git clone http://bugs.sleepanarchy.com/fec.git

Create a new virtualenv::

    mkvirtualenv fec

Install the ``lessc`` ``LESS`` compiler for your system::

    # Arch Linux
    pacman -S nodejs-less
    # Debian
    apt-get install node-less

Install python dependencies w/ ``pip``::

    pip install -r requirements/local.txt

Set environmental variables to match your configuration::

    export DJANGO_SECRET_KEY=fourtytwo
    export DJANGO_SETTINGS_MODULE=fec.settings.local
    export DB_NAME=FEC
    export DB_USER=myuser

Create the database and optionally preload some initial data::

    cd fec
    ./manage.py createdb --noinput
    ./manage.py loaddata homepage/fixtures/homepage_original.json
    ./manage.py loaddata fec/fixtures/nav_pages_original.json

Finally you can start the dev server::

    ./manage.py runserver 0.0.0.0:8000


BrowserSync
------------

BrowserSync lets you sync up actions betweens browsers & automatically reloads
your browsers when a source file has been modified.

You'll need ``npm`` & ``gulp`` installed::

    pacman -S npm
    npm install -g gulp

Then install our Gulp dependencies & run ``gulp`` in the project's base
directory::

    npm install
    gulp

Gulp will start the Django server for you along with a proxy server that
injects the BrowserSync code at http://localhost:8010.


Documentation
--------------

You can read the documentation at http://fecwebsite.readthedocs.org/.

To build the documentation locally::

    cd docs/
    make html

Then read the docs at ``docs/_build/html/index.html``.


Tests
------

Install the test dependencies::

    pip install -r requirements/test.txt

Then you can start the test runner::

    cd fec
    py.test

Once completed, the test runner will monitor for file changes & re-run the test
suite.

You can also run a subset of the tests::

    py.test communities/tests.py -k CommunityDetail


Deployment
----------

The documentation contains a `guide for deploying on Debian 7 (Wheezy)
<https://fecwebsite.readthedocs.org/en/latest/appendix_debian.html>`_ using
memcached, postgreSQL, uWSGI and Apache.


Contribute
-----------

Template overrides and sitewide items go in ``fec``.

Write tests, maintain 100% test coverage. Update docs when necessary.

Run ``prospector`` in the base directory to check out your code style.


License
--------

GPLv3
