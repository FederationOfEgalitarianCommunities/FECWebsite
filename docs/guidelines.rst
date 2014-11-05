.. _Contribution Guidelines:

========================
Contribution Guidelines
========================

This section describes development standards and best practices within the
project.


Code Conventions
=================

The :pep:`8` is our baseline for coding style.

In short we use:

* 4 spaces per indentation
* 79 characters per line
* One import per line, grouped in the following order: standard library, 3rd
  party imports, local application imports
* One statement per line
* Docstrings for all public modules, functions, classes and methods.

The following naming conventions should be followed:

* Class names use CapitalWords
* Function names are lowercase, with words separated by underscores
* Use ``self`` and ``cls`` for first argument to instance and class methods,
  respectively.
* Non-public methods and variables should be prefixed with an underscore
* Constants in all uppercase.

Code should attempt to be idiomatic/pythonic, for example:

* Use list, dict and set comprehensions.
* Test existence in a sequence with ``in``.
* Use ``enumerate`` instead of loop counters.
* Use ``with ... as ...`` for context managers.
* Use ``is`` to compare against ``None`` instead of ``==``.
* Use parenthesis instead of backslashes for line continuations.

For more information and full coverage of conventions, please read :pep:`8`,
:pep:`257`, :pep:`20` and the `Django Coding Style Documentation`_.

There are tools available to help assess compliance to these conventions, such
as ``pep8`` and ``pylint``. Both of these tools are installed via ``pip``:

.. code-block:: bash

    $ pip install pep8
    $ pip install pylint

You may then run ``pep8`` on files to determine their compliance:

.. code-block:: bash

    $ pep8 core/utils.py
    core/utils.py:26:80: E501 line too long (116 > 79 characters)


Version Control
================

We use Git as our Version Control System.


Branches
---------

We have 2 long-term public branches:

* ``master`` - The latest stable release. This branch should be tagged with a
  new version number every time a branch is merged into it.
* ``develop`` - The release currently in development. New features and releases
  originate from this branch.

There are also multiple short-term supporting branches:

* ``hotfix`` - Used for immediate changes that need to be pushed out into
  production. These branches should originate from ``master`` and be merged
  into ``master`` and either the ``develop`` or current ``release`` if one
  exists.
* ``feature`` - Used for individual features and bug fixes, these branches are
  usually kept on local development machines. These should originate from and
  be merged back into ``develop``.
* ``release`` - Used for preparing the ``develop`` branch for merging into
  ``master``, creating a new release. These branches should originate from
  ``develop`` and be merged back into ``develop`` and ``master``. Releases
  should be created when all new features for a version are finished. Any new
  commits should only contain code refactoring and bug fixes.

This model is adapted from `A Successful Git Branching Model`_, however we use
a linear history instead of a branching history, so the ``--no-ff`` option
should be omitted during merges.


Commit Messages
----------------

Commit messages should follow the format described in `A Note About Git Commit
Messages`_. They should generally follow the following format::

    [TaskID#] Short 50 Char or Less Title

    Explanatory text or summary describing the feature or bugfix, capped
    at 72 characters per line, written in the imperative.

    Bullet points are also allowed:

    * Add method `foo` to `Bar` class
    * Modify `Base` class to be abstract
    * Remove `foobaz` method from `Bar` class
    * Refactor `bazfoo` function

    Refs/Closes/Fixes #TaskID: Task Name in Bug Tracker

For example::

    [#367] Customize General Layout & Home Page

    * Add the core app and a SeleniumTestCase class to the core.utils module
      to automatically start a live server and create a remote selenium
      driver.
    * Add the functional_tests.general_page_tests module to test elements
      that should be on every page.
    * Add the functional_tests.home_page_tests module to test elements that
      should appear on the home page.
    * Add basic site customizations, like modifying the title, tagline and
      homepage content.
    * Add requirements files for test and local environments.

    * Modify manage.py to use the thefec module's settings files
    * Move the functional tests into their own module.

    * Remove the right sidebar.
    * Remove the lettuce applications.
    * Remove extraneous files from the thefec module.

    Closes #367: Create Initial project


Workflow
---------

The general workflow we follow is based on `A Git Workflow for Agile Teams`_.

Work on a new task begins by branching from ``develop``. Feature branch names
should be in the format of ``tasknumber-short-title-or-name``:

.. code-block:: bash

    $ git checkout -b 142-add-account-history develop


Commits on this branch should be early and often. These commit messages are not
permanent and do not have to use the format specified above.

You should fetch and rebase against the upstream repository often in order to
prevent merging conflicts:

.. code-block:: bash

    $ git fetch origin develop
    $ git rebase origin/develop

When work is done on the task, you should rebase and squash your many commits
into a single commit:

.. code-block:: bash

    $ git rebase -i origin/develop

You may then choose which commits to reorder, squash or reword.

.. warning:: Only rebase commits that have not been published to public
    branches. Otherwise problems will arise in every other user's local
    repository. NEVER rewrite public branches and NEVER force a push unless
    you know EXACTLY what you are doing, and have preferably backed up the
    upstream repository.

Afterwards, merge your changes into ``develop`` and push your changes to the
upstream repository:

.. code-block:: bash

    $ git checkout develop
    $ git merge 142-add-account-history
    $ git push origin develop


Preparing a Release
--------------------

A Release should be forked off of develop into its own branch once all
associated features are completed. A ``release`` branch should contain only
bugfixes and version bumps.

#. Fork the ``release`` branch off of the ``develop`` branch:

   .. code-block:: bash

       $ git checkout -b release-1.2.0 develop

#. Branch, Fix and Merge any existing bugs.
#. Bump the version number and year in ``setup.py`` and
   ``docs/source/conf.py``.
#. Commit the version changes:

   .. code-block:: bash

       $ git commit -a -m "Prepare v1.2.0 Release"

#. Create a new annotated and signed Tag for the commit:

   .. code-block:: bash

       $ git tag -s -a v1.2.0

    The annotation should contain the release's name and number, and optionally
    a short description::

        Version 1.2.0 Release - Trip Entry Form

        This release adds a Trip Entry form for Communards and a Trip Approving
        form for Accountants.

#. Merge the branch into the ``master`` branch and push it upstream:

   .. code-block:: bash

       $ git checkout master
       $ git merge release-1.2.0
       $ git push origin master
       $ git push --tags origin master

#. Make sure to merge back into the ``develop`` branch as well:

   .. code-block:: bash

       $ git checkout develop
       $ git merge release-1.2.0
       $ git push origin develop

#. You can then remove the ``release`` branch from your local repository:

   .. code-block:: bash

       $ git branch -d release-1.2.0


Version Numbers
================

Each release will be tagged with a version number, using the MAJOR.MINOR.PATCH
`Semantic Versioning`_ format and specifications.

These version numbers indicate the changes to the public API.

The PATCH number will be incremented if a new version contains only
backwards-compatible bug fixes.

The MINOR number is incremented for new, backwards-compatible functionality and
marking any new deprecations. Increasing the MINOR number should reset the
PATCH number to 0.

The MAJOR number is incremented if ANY backwards incompatible changes are
introduced to the public API. Increasing the MAJOR number should reset
the MINOR and PATCH numbers to 0.

Pre-release versions may have additional data appended to the version, e.g.
``1.0.1-alpha`` or ``2.1.0-rc``.

The first stable release will begin at version 1.0.0, any versions before this
are for initial development and should be not be considered stable.

For more information, please review the `Semantic Versioning Specification`_.


Documentation
==============

This documentation is written in `reStructuredText`_  and created using the
`Sphinx`_ Documentation Generator. Sphinx's ``autodoc`` module is used to
create the API specifications of the application by scraping
docstrings(:pep:`257`).

Each class, function, method and global should have an accurate docstring for
Sphinx to use.

Each feature or bug fix should include all applicable documentation changes.

To build the Documentation, install the prerequisites then run the make command
to generate either html or pdf output:

.. code-block:: bash

    $ pip install -r requirements/local.txt
    $ cd docs/
    $ make html; make latexpdf

The output files will be located in the ``docs/_build`` directory.



.. _A Note About Git Commit Messages:
    http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html

.. _A Successful Git Branching Model:
    http://nvie.com/posts/a-successful-git-branching-model/

.. _A Git Workflow for Agile Teams:
    http://reinh.com/blog/2009/03/02/a-git-workflow-for-agile-teams.html

.. _Django Coding Style Documentation:
    http://docs.djangoproject.com/en/1.4/internals/contributing/writing-code/coding-style/

.. _reStructuredText:
    http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html

.. _Semantic Versioning:
.. _Semantic Versioning Specification: http://semver.org/

.. _Sphinx: http://sphinx-doc.org/
