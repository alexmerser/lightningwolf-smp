Sentry
======

::

    $ apt-get install python-virtualenv

::

    $ mkdir /var/www/sentry

::

    $ cd /var/www/sentry

::

    $ virtualenv sentry-ve-`date +%F` -p python2.7 --no-site-packages --distribute
    $ ln -s sentry-ve-`date +%F` sentry-ve

Then use:

::

    $ source sentry-ve/bin/activate


::

    $ pip install sentry[mysql]


http://sentry.readthedocs.org/en/latest/quickstart/index.html#install-sentry