.. _basic:

Basic instance setup
====================

Localisation
------------

For example I'm leave in Poland then I need to make some additional instalations and configurations:

Language
^^^^^^^^

1. Install needed package ::

    $ sudo apt-get install  language-pack-pl-base

2. Recinfigure locales ::

    $ sudo dpkg-reconfigure locales

3. Check configuration ::

    $ locale -a
    $ locale

4. Update locale settings ::

    $ sudo update-locale LANG=pl_PL.UTF-8 LC_MESSAGES=POSIX

Timezone
^^^^^^^^

1. Set timezone ::

    $ sudo echo "Europe/Warsaw" | sudo tee /etc/timezone

2. Reconfigure timezone data ::

    $ sudo dpkg-reconfigure --frontend noninteractive tzdata


Server Hostname
---------------

1. Modify server **hostname**, for our example it will be **wolf.lightningwolf.net**::

    $ sudo hostname wolf.lightningwolf.net

2. Now set the contents of ``/etc/hostname`` and ``/etc/mailname`` to be the ``wolf.lightningwolf.net``

3. And add your hostname to the first line of ``/etc/hosts``

   | 127.0.0.1 wolf.lightningwolf.net localhost

