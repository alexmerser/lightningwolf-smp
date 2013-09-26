lightningwolf-smp - Development
===============================

Requirements
------------

Python
``````
All Python requirements are in `requirements.txt` file.


Development Installation from GIT
---------------------------------

Repository cloning
``````````````````

::

    $ cd ~
    $ git clone https://github.com/lightningwolf/lightningwolf-smp.git

Virtualenv
``````````

Standard method
'''''''''''''''

First create one:

::

    $ virtualenv lightningwolf-smp-`date +%F` -p python2.7 --no-site-packages --distribute
    $ ln -s lightningwolf-smp-`date +%F` lightningwolf-smp-ve

Then use:

::

    $ source lightningwolf-smp-ve/bin/activate

Virtualenvwrapper
'''''''''''''''''

First create one:

::

    $ mkvirtualenv --distribute lightningwolf-smp

Using virtualenvs with virtualenvwrapper is easy:

::

    $ workon lightningwolf-smp


Finalize install
````````````````

**Prior to this step, make sure that you are working in an environment virtualenv.**

::

    $ cd lightningwolf-smp
    $ python setup.py develop


Configuration
-------------

Database
````````

Create Mysql Databese with user


#. Create config folder and file in it:

::

    $ mkdir config
    $ touch config/config.py

#. Sample Configuration:

::

    #!/usr/bin/env python
    # coding=utf8

    DEBUG = True
    SECRET_KEY = '<write something here>'
    SQLALCHEMY_DATABASE_URI = 'mysql://<user>:<pass>@<ip or hostname>/<db name>'
    SENTRY_DSN = '<Nothing or Your Sentry DSN>'


#. Use this config in virtual environment:

::

    $ export LIGHTNINGWOLF_SETTINGS=<path to config.py file>

Or for example start application with ``--config`` option

::

    $ smp --config=<path to config.py file> start

**TODO**