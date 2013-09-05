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

**TODO**