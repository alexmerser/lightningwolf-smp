Sentry
======

Best documentation are in the source of this document `Sentry docs <http://sentry.readthedocs.org/en/latest/quickstart/index.html#install-sentry>`_.
This one is a little modified simplified version of it.

::

    $ apt-get install python-virtualenv

::

    $ mkdir /var/www/sentry

::

    $ cd /var/www/sentry

Now make no access to this folder by creating ``.htaccess`` file with those settings

::

    RewriteEngine Off
    deny from all

::

    $ virtualenv sentry-ve-`date +%F` -p python2.7 --no-site-packages --distribute
    $ ln -s sentry-ve-`date +%F` sentry-ve

Then use:

::

    $ source sentry-ve/bin/activate


::

    $ pip install sentry[mysql]


Initializing the Configuration
------------------------------

Now you'll need to create the default configuration. To do this, you'll use the ``init`` command
You can specify an alternative configuration path as the argument to init, otherwise it will use
the default of ``~/.sentry/sentry.conf.py``.

::

    # the path is optional
    sentry init /etc/sentry.conf.py

The configuration for the server is based on ``sentry.conf.server``, which contains a basic Django project
configuration, as well as the default Sentry configuration values. It defaults to SQLite, however **SQLite
is not a fully supported database and should not be used in production**.

::

    # ~/.sentry/sentry.conf.py

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',  # We suggest PostgreSQL for optimal performance
            'NAME': 'sentry',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': '',
            'PORT': '',
            'OPTIONS': {
                'autocommit': True,
            }
        }
    }

    # No trailing slash!
    SENTRY_URL_PREFIX = 'http://sentry.example.com'

    # SENTRY_KEY is a unique randomly generated secret key for your server, and it
    # acts as a signing token
    SENTRY_KEY = '0123456789abcde'

    SENTRY_WEB_HOST = '0.0.0.0'
    SENTRY_WEB_PORT = 9000
    SENTRY_WEB_OPTIONS = {
        'workers': 3,  # the number of gunicorn workers
        'secure_scheme_headers': {'X-FORWARDED-PROTO': 'https'},  # detect HTTPS mode from X-Forwarded-Proto header
    }


Configure Outbound Mail
-----------------------

Several settings exist as part of the Django framework which will configure your outbound mail server. For the
standard implementation, using a simple SMTP server, you can simply configure the following::

    EMAIL_HOST = 'localhost'
    EMAIL_HOST_PASSWORD = ''
    EMAIL_HOST_USER = ''
    EMAIL_PORT = 25
    EMAIL_USE_TLS = False

Being that Django is a pluggable framework, you also have the ability to specify different mail backends. See the
`official Django documentation <https://docs.djangoproject.com/en/1.3/topics/email/?from=olddocs#email-backends>`_ for
more information on alternative backends.

Running Migrations
------------------

Sentry provides an easy way to run migrations on the database on version upgrades. Before running it for
the first time you'll need to make sure you've created the database.

Once done, you can create the initial schema using the ``upgrade`` command::

    sentry --config=/etc/sentry.conf.py upgrade

**It's very important that you create the default superuser through the upgrade process. If you do not, there is
a good chance you'll see issues in your initial install.**

If you did not create the user on the first run, you can correct this by doing the following::

    # create a new user
    sentry --config=/etc/sentry.conf.py createsuperuser

    # run the automated repair script
    sentry --config=/etc/sentry.conf.py repair --owner=<username>

All schema changes and database upgrades are handled via the ``upgrade`` command, and this is the first
thing you'll want to run when upgrading to future versions of Sentry.

.. note:: Internally, this uses `South <http://south.aeracode.org>`_ to manage database migrations.

Starting the Web Service
------------------------

Sentry provides a built-in webserver (powered by gunicorn and eventlet) to get you off the ground quickly,
also you can setup Sentry as WSGI application, in that case skip to section `Running Sentry as WSGI application`.

To start the webserver, you simply use ``sentry start``. If you opted to use an alternative configuration path
you can pass that via the --config option.

::

  # Sentry's server runs on port 9000 by default. Make sure your client reflects
  # the correct host and port!
  sentry --config=/etc/sentry.conf.py start

You should now be able to test the web service by visiting `http://localhost:9000/`.
