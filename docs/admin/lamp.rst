.. _lamp:

LAMP - Linux Apache MySQL PHP
=============================

Installation
------------

First update packages system

::

    $ apt-get update
    $ apt-get upgrade

Then install base system

::

    $ apt-get install lamp-server^

Now we add some additional important packages

::

    $ apt-get install php-apc php5-memcache php5-memcached php5-curl php5-gd php-xml-parser php5-dev

Memcache is also important

::

    $ apt-get install memcached

::

    $ service mysql restart

Also phpMyAdmin

::

    apt-get install phpmyadmin php5-mcrypt

When ask chose Apache and remeber to give MySQL root password in basic configuration process.


And nice to have for Symfony2

::

    apt-get install php5-intl

And for other projects:

::

    apt-get install imagemagick php5-imagick libmagickcore5-extra php5-tidy

In Ubuntu 13.10

::

    sudo ln -s /etc/php5/conf.d/mcrypt.ini /etc/php5/mods-available
    sudo php5enmod mcrypt
    sudo service apache2 restart

Configuration
-------------

PHP Configuration
^^^^^^^^^^^^^^^^^

The default configuration for PHP and the additional packages mentioned above is sufficient for most casual usage.
So unless you have something complicated or high-powered in mind, you should probably only change the expose_php setting
in ``/etc/php5/apache2/php.ini`` and ``/etc/php5/cli/php.ini``. Set it to "Off"

::

    ; Decides whether PHP may expose the fact that it is installed on the server
    ; (e.g. by adding its signature to the Web server header).  It is no security
    ; threat in any way, but it makes it possible to determine whether you use PHP
    ; on your server or not.
    ; http://php.net/expose-php
    expose_php = Off

Nest in this files you should set-up **timezone**. In my examle

::

    [Date]
    ; Defines the default timezone used by the date functions
    ; http://php.net/date.timezone
    date.timezone = "Europe/Warsaw"

Apache Configuration
^^^^^^^^^^^^^^^^^^^^

Firstly configure the following lines in ``/etc/apache2/conf.d/security` to minimize the information that Apache gives
out in its response headers

::

    #
    # ServerTokens
    # This directive configures what you return as the Server HTTP response
    # Header. The default is 'Full' which sends information about the OS-Type
    # and compiled in modules.
    # Set to one of:  Full | OS | Minimal | Minor | Major | Prod
    # where Full conveys the most information, and Prod the least.
    #
    ServerTokens Prod

    #
    # Optionally add a line containing the server version and virtual host
    # name to server-generated pages (internal error documents, FTP directory
    # listings, mod_status and mod_info output etc., but not CGI generated
    # documents or custom error documents).
    # Set to "EMail" to also include a mailto: link to the ServerAdmin.
    # Set to one of:  On | Off | EMail
    #
    ServerSignature Off

Make sure that mod_rewrite, mod_ssl, and the default SSL virtual host is enabled - you'll need these line items to be
able to force visitors to use HTTPS.

::

    a2enmod rewrite ssl
    a2ensite default-ssl

The default site configuration in ``/etc/apache2/sites-available/default`` can be edited to look something like this for
the sake of simplicity

::

    <VirtualHost *:80>
      ServerAdmin webmaster@localhost

      DocumentRoot /var/www
      <Directory "/">
        Options FollowSymLinks
        AllowOverride All
      </Directory>

      ErrorLog ${APACHE_LOG_DIR}/error.log

      # Possible values include: debug, info, notice, warn, error, crit,
      # alert, emerg.
      LogLevel warn

      CustomLog ${APACHE_LOG_DIR}/access.log combined
    </VirtualHost>

But of course your taste and needs may vary. Keeping the same simple approach, the upper portion of the SSL
configuration in ``/etc/apache2/sites-available/default-ssl`` can be set up as follows

::

    <IfModule mod_ssl.c>
      <VirtualHost _default_:443>
        ServerAdmin webmaster@localhost

        DocumentRoot /var/www
        <Directory "/">
          Options FollowSymLinks
          AllowOverride All
        </Directory>

        ErrorLog ${APACHE_LOG_DIR}/error.log

        # Possible values include: debug, info, notice, warn, error, crit,
        # alert, emerg.
        LogLevel warn

        CustomLog ${APACHE_LOG_DIR}/ssl_access.log combined

        #   SSL Engine Switch:
        #   Enable/Disable SSL for this virtual host.
        SSLEngine on
        #

        # ... more default SSL configuration ...

        # You will probably need to change this next Directory directive as well
        # in order to match the earlier one.
        <Directory "/">
          SSLOptions +StdEnvVars
        </Directory>

        # ... yet more default SSL configuration ...

      </VirtualHost>
    </IfModule>

To push visitors to HTTPS, put something similar to the following snippet into ``/var/www/.htaccess``, for our example
it will be **wolf.lightningwolf.net**

::

    RewriteEngine On
    RewriteCond %{SERVER_PORT} 80
    RewriteRule ^(.*) https://wolf.lightningwolf.net/$1 [L]

Now create folder for customers pages

::

    $ mkdir /var/www/customers

and set no access in this folder by creating ``.htaccess`` file with this settings

::

    RewriteEngine Off
    deny from all


MySQL Configuration
^^^^^^^^^^^^^^^^^^^

Create file ``/etc/mysql/conf.d/utf8_charset.cnf`` and put into it

::

    [mysqld]
    character-set-server=utf8
    collation-server=utf8_general_ci

Then restart MySQL server

::

    $ service mysql restart

Memcache Configuration
^^^^^^^^^^^^^^^^^^^^^^

The default configuration file at ``/etc/memcached.conf`` is good enough for a small server: it locks down access to
localhost and provides generally sensible configuration parameter values. If you are building a larger machine for heavy
usage, you will probably want to bump the memory allocation to be higher than the default of 64M

::

    # Start with a cap of 64 megs of memory. It's reasonable, and the daemon default
    # Note that the daemon will grow to this size, but does not start out holding this much
    # memory
    -m 64

PhpMyAdmin Configuration
^^^^^^^^^^^^^^^^^^^^^^^^

The best method is to restrict access for phpMyAdmin to given IPs. Modify ``/etc/phpmyadmin/apache.conf`` file, for our
example it will use **wolf.lightningwolf.net** in settings

::

    <Directory /usr/share/phpmyadmin>
        Options FollowSymLinks
        DirectoryIndex index.php

        # Dodajemy przekierowanie na https
        RewriteEngine On
        RewriteCond %{SERVER_PORT} 80
        RewriteRule ^(.*) https://wolf.lightningwolf.net/phpmyadmin/$1 [L]

        # Dodajemy nasze restrykcje na IP
        Order allow,deny
        Allow from 192.168.1.0/24
        Allow from 127

        <IfModule mod_php5.c>
            AddType application/x-httpd-php .php

            php_flag magic_quotes_gpc Off
            php_flag track_vars On
            php_flag register_globals Off
            php_admin_flag allow_url_fopen Off
            php_value include_path .
            php_admin_value upload_tmp_dir /var/lib/phpmyadmin/tmp
            php_admin_value open_basedir /usr/share/phpmyadmin/:/etc/phpmyadmin/:/var/lib/phpmyadmin/:/usr/share/php/php-gettext
        </IfModule>
    </Directory>

Restart all services and check them.
