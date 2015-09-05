Debian 7 (Wheezy) Deployment Guide
==================================

This section covers deploying the website on Debian 7(Wheezy). It assumes you
have a working apache configuration and are logged in as ``thefec``.


Install & Configure PostgreSQL
------------------------------

Start by installing the postgreSQL server & client. Development libraries are
required for the python postgreSQL library:

.. code-block:: bash

    $ sudo apt-get install postgresql postgresql-server postgresql-server-dev-9.1

Next, become the ``postgres`` user and create a new database and user:

.. code-block:: bash

    $ sudo su - postgres
    $ createuser -DERPS thefec      # No DB/user creation privleges, not a superuser, encrypt the password
    $ createdb fec_website -O thefec
    $ logout


Install Memcached
-----------------

Memcached is used for caching. All you need to do is install it to get it
working, it will automatically start a server at ``127.0.0.1:11211``:

.. code-block:: bash

    $ sudo apt-get install memcached


Enable Wheezy Backports & Install the LESS Compiler
---------------------------------------------------

``lessc`` takes LESS source files and converts them to CSS. To get the package
in Debian 7, we need to enable the ``wheezy-backports`` repository. To do this,
add the following line to the end of ``/etc/apt/sources.list``::

    deb http://http.debian.net/debian wheezy-backports main

Then you can update your package list & install ``lessc``:

.. code-block:: bash

    $ sudo apt-get update
    $ sudo apt-get -t wheezy-backports install node-less


Install & Create Python Virtual Environment
-------------------------------------------

A virtual environment will let us separate our dependencies from the system's
python libraries:

.. code-block:: bash

    $ sudo apt-get install python-virtualenv
    $ virtualenv ~/WebsiteEnv

We'll create a bash script at ``~/load_website_env.sh`` to set environmental
variables that configure the website(database name, password, secret key, etc.):

.. code-block:: bash

    # ~/load_website_env.sh
    source ~/WebsiteEnv/bin/activate

    export DB_NAME='fec_website'
    export DB_USER='thefec'
    export DB_PASS=YOUR_PASSWORD

    export ALLOWED_HOST='www.thefec.org'
    export DJANGO_SECRET_KEY=YOUR_SECRET_KEY
    export DJANGO_SETTINGS_MODULE='fec.settings.production'
    export CACHE_PREFIX='FECprod'

Since this contains our database user's password, we'll make sure only we can
run/read/write it:

.. code-block:: bash

    $ chmod 700 ~/load_website_env.sh


Download & Setup Application
----------------------------

First we'll need ``git`` to pull the source code and some image libraries:

.. code-block:: bash

    $ sudo apt-get install git libjpeg-dev libfreetype6-dev

Activate our virtual environment, grab the source & install the python
dependencies:

.. code-block:: bash

    $ source ~/load_website_env.sh
    $ cd ~
    $ git clone http://bugs.sleepanarchy.com/fec.git ~/website
    $ cd ~/website
    $ pip install -r requirements/base.txt

Create the database schema and load the initial data if you have any:

.. code-block:: bash

    $ cd ~/website/fec
    $ ./manage.py migrate
    $ ./manage.py loaddata ~/full_dump.json

Collect the static files & link it to our public HTML directory:

.. code-block:: bash

    $ ./manage.py collectstatic
    $ ln -s ~/website/fec/static ~/htdocs/static


Install & Configure Python Server
---------------------------------

Dynamic requests will be served by the ``uWSGI`` server and proxied by apache.
Static files like images, CSS and JavaScript will be served by apache.

Start by installing ``uWSGI`` along with some libraries required for gzipping:

.. code-block:: bash

    $ sudo apt-get install uwsgi uwsgi-plugin-python libpcre3-dev libz-dev

Add the following configuration to
``/etc/uwsgi/apps-available/fec-website.ini``:

.. code-block:: ini

    [uwsgi]
    uid = thefec
    gid = www-data
    chdir = /home/thefec/website/fec

    plugin = python2,transformation_gzip
    pythonpath = /home/thefec/WebsiteEnv/lib/python2.7/site-packages/
    pythonpath = /usr/lib/python2.7
    virtualenv = /home/thefec/WebsiteEnv
    no-site=True

    socket = 127.0.0.1:3032
    master = true
    workers = 4
    max-requests = 5000
    vacuum = True

    pidfile = /tmp/fec-website.pid
    touch-reload = /tmp/fec-website.touch

    env = DJANGO_SETTINGS_MODULE=fec.settings.production
    env = DJANGO_SECRET_KEY=YOUR_SECRET_KEY
    env = DB_NAME=fec_website
    env = DB_USER=thefec
    env = DB_PASS=YOUR_PASSWORD
    env = ALLOWED_HOST=www.thefec.org
    env = CACHE_PREFIX=FECprod
    wsgi-file = /home/thefec/website/fec/fec/wsgi.py

    # route to gzip if supported
    route-if = contains:${HTTP_ACCEPT_ENCODING};gzip goto:mygzipper
    route-run = last:

    route-label = mygzipper
    route = ^/$ gzip:

Link the file to ``apps-enabled`` to enable it, restart uwsgi, then ``touch``
the touch-file to restart the python server:

.. code-block:: bash

    $ sudo ln -s /etc/uwsgi/apps-available/fec-website.ini /etc/uwsgi/apps-enabled/
    $ sudo service uwsgi restart
    $ touch /tmp/fec-website.touch


Configure Virtual Host
----------------------

First we need to install the apache module for uWSGI:

.. code-block:: bash

    $ sudo apt-get install libapache2-mod-uwsgi

Then add the following configuration to
``/etc/apache2/sites-available/thefec.org.conf``:

.. code-block:: apacheconf

    <VirtualHost 72.249.12.147:80>
        ServerName www.thefec.org

        DocumentRoot /home/thefec/website/fec

        ErrorLog /home/thefec/logs/error_log
        CustomLog /home/thefec/logs/access_log common

        Alias /static /home/thefec/htdocs/static
        <Directory /home/thefec/htdocs/static>
            Options Indexes FollowSymLinks MultiViews
            allow from all
            AllowOverride All
        </Directory>

        # Redirect requests to the python server
        <Location "/">
            Options FollowSymLinks Indexes
            SetHandler uwsgi-handler
            uWSGISocket 127.0.0.1:3032
        </Location>
        # Except for requests to /static/
        <Location /static>
            SetHandler none
            allow from all
        </Location>

        # Cache all the things
        ExpiresActive On
        ExpiresByType text/html "access plus 5 minutes"
        ExpiresByType text/css "access plus 10 years"
        ExpiresByType text/javascript "access plus 10 years"
        ExpiresByType application/x-javascript "access plus 10 years"
        ExpiresByType text/javascript "access plus 10 years"
        ExpiresByType application/javascript "access plus 10 years"
        ExpiresByType image/jpg "access plus 10 years"
        ExpiresByType image/gif "access plus 10 years"
        ExpiresByType image/jpeg "access plus 10 years"
        ExpiresByType image/png "access plus 10 years"
        ExpiresByType image/x-icon "access plus 10 years"
        ExpiresByType image/icon "access plus 10 years"
        ExpiresByType application/x-ico "access plus 10 years"
        ExpiresByType application/ico "access plus 10 years"

        # Gzip all the things
        <IfModule mod_deflate.c>
            AddOutputFilterByType DEFLATE text/text text/html text/plain text/xml text/css
            AddOutputFilterByType DEFLATE application/x-javascript application/javascript image/x-icon
        </IfModule>

        # Seperate browser caching for gzip-encoded things
        <FilesMatch ".(js|css|xml|gz|html)$">
            Header append Vary: Accept-Encoding
        </FilesMatch>
    </VirtualHost>


    # Redirect other domains to www.thefec.org, preserving the URL path
    <VirtualHost 72.249.12.147:80>
        ServerName thefec.org
        ServerAlias *.thefec.org
        ServerAlias thefec.skyhouseconsulting.com
        Redirect permanent / http://www.thefec.org/
    </VirtualHost>

Then enable the site and restart apache:

.. code-block:: bash

    $ sudo a2ensite thefec.org
    $ sudo apache2ctl -k restart

The site should now be visible at http://www.thefec.org


Setup Cronjobs to Optimize Images
---------------------------------

We'll run two commands daily to compress & optimize uploaded jpeg & png images.
First install the optimizing tools:

.. code-block:: bash

    $ sudo apt-get install optipng libjpeg-progs

Edit the cronjobs by running ``crontab -e`` and adding the following lines:

.. code-block:: cron

    # Optimize Images Uploaded to the FEC Website
    @daily find /home/thefec/htdocs/static/media -type f -iname "*.png" -exec optipng -o7 {} \; > /dev/null 2>&1
    @daily find /home/thefec/htdocs/static/media -type f -iname "*.jpeg" -o -iname "*.jpg" -exec jpegtran -copy none -progressive -optimize -outfile {} {} \; > /dev/null 2>&1
