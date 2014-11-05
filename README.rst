Federation of Egalitarian Communities Website
==============================================

This is the Mezzanine project that powers ``thefec.org``.

Quickstart
-----------

Clone source code::

    git clone http://bugs.sleepanarchy.com/fec.git

Create a new virtualenv::

    mkvirtualenv fec

Install python dependencies w/ ``pip``::

    pip install -r requirements/local.txt

Build the full documentation::

    cd docs/
    make html

Start the dev server::

    cd ../fec
    ./manage.py runserver 0.0.0.0:8000

Read the documentation at ``docs/_build/html/index.html`` for more information.
