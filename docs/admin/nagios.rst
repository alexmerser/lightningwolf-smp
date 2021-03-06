.. _nagios:

Nagios
======

Installation
------------

First, on `server01` install the `nagios` package. In a terminal enter

::

    $ sudo apt-get install nagios3 nagios-nrpe-plugin

You will be asked to enter a password for the `nagiosadmin` user. The user's credentials are stored in
``/etc/nagios3/htpasswd.users``. To change the `nagiosadmin` password, or add additional users to the Nagios CGI
scripts, use the `htpasswd` that is part of the `apache2-utils` package.

For example, to change the password for the `nagiosadmin` user enter

::

    $ sudo htpasswd /etc/nagios3/htpasswd.users nagiosadmin

To add a user:

::

    $ sudo htpasswd /etc/nagios3/htpasswd.users steve

Next, on server02 install the `nagios-nrpe-server` package. From a terminal on `server02` enter

::

    $ sudo apt-get install nagios-nrpe-server

::

    NRPE allows you to execute local checks on remote hosts. There are other ways of accomplishing this through other Nagios plugins as well as other checks.

Configuration Overview
----------------------

There are a couple of directories containing Nagios configuration and check files:

1. ``/etc/nagios3``: contains configuration files for the operation of the `nagios` daemon, CGI files, hosts, etc.
2. ``/etc/nagios-plugins``: houses configuration files for the service checks.
3. ``/etc/nagios``: on the remote host contains the `nagios-nrpe-server` configuration files.
4. ``/usr/lib/nagios/plugins/``: where the check binaries are stored. To see the options of a check use the -h option.
5. For example: ``/usr/lib/nagios/plugins/check_dhcp -h``

There are a plethora of checks Nagios can be configured to execute for any given host. For this example Nagios will be
configured to check disk space, DNS, and a MySQL hostgroup. The DNS check will be on `server02`, and the MySQL hostgroup
will include both `server01` and `server02`.

Additionally, there are some terms that once explained will hopefully make understanding Nagios configuration easier:

1. `Host`: a server, workstation, network device, etc that is being monitored.
2. `Host Group`: a group of similar hosts. For example, you could group all web servers, file server, etc.
3. `Service`: the service being monitored on the host. Such as HTTP, DNS, NFS, etc.
4. `Service Group`: allows you to group multiple services together. This is useful for grouping multiple HTTP for example.
5. `Contact`: person to be notified when an event takes place. Nagios can be configured to send emails, SMS messages, etc.

By default Nagios is configured to check HTTP, disk space, SSH, current users, processes, and load on the `localhost`.
Nagios will also `ping` check the `gateway`.

Large Nagios installations can be quite complex to configure. It is usually best to start small, one or two hosts, get things configured the way you like then expand.

Configuration
-------------

Step 1
^^^^^^

1. First, create a host configuration file for `server02`. Unless otherwise specified, run all these commands on
`server01`. In a terminal enter:

::

    $ sudo cp /etc/nagios3/conf.d/localhost_nagios2.cfg /etc/nagios3/conf.d/server02.cfg

::

    In the above and following command examples, replace "server01", "server02" 172.18.100.100, and 172.18.100.101 with
    the host names and IP addresses of your servers.

2. Next, edit ``/etc/nagios3/conf.d/server02.cfg``:

::

    define host{
            use                     generic-host  ; Name of host template to use
            host_name               server02
            alias                   Server 02
            address                 172.18.100.101
    }

    # check DNS service.
    define service {
            use                             generic-service
            host_name                       server02
            service_description             DNS
            check_command                   check_dns!172.18.100.101
    }

3. Restart the nagios daemon to enable the new configuration:

::

    $ sudo /etc/init.d/nagios3 restart

Step 2
^^^^^^

1. Now add a service definition for the MySQL check by adding the following to
``/etc/nagios3/conf.d/services_nagios2.cfg``:

::

    # check MySQL servers.
    define service {
            hostgroup_name        mysql-servers
            service_description   MySQL
            check_command         check_mysql_cmdlinecred!nagios!secret!$HOSTADDRESS
            use                   generic-service
            notification_interval 0 ; set > 0 if you want to be renotified
    }

2. A mysql-servers hostgroup now needs to be defined. Edit ``/etc/nagios3/conf.d/hostgroups_nagios2.cfg`` adding:

::

    # MySQL hostgroup.
    define hostgroup {
            hostgroup_name  mysql-servers
                    alias           MySQL servers
                    members         localhost, server02
            }

3. The Nagios check needs to authenticate to MySQL. To add a nagios user to MySQL enter:

::

    $ mysql -u root -p -e "create user nagios identified by 'secret';"

::

    The nagios user will need to be added all hosts in the mysql-servers hostgroup.

4. Restart nagios to start checking the MySQL servers.

    $ sudo /etc/init.d/nagios3 restart

Step 3
^^^^^^

1. Lastly configure NRPE to check the disk space on `server02`.

On `server01` add the service check to ``/etc/nagios3/conf.d/server02.cfg``:

::

    # NRPE disk check.
    define service {
            use                     generic-service
            host_name               server02
            service_description     nrpe-disk
            check_command           check_nrpe_1arg!check_all_disks!172.18.100.101
    }

2. Now on `server02` edit ``/etc/nagios/nrpe.cfg`` changing:

::

    allowed_hosts=172.18.100.100

And below in the command definition area add:

::

    command[check_all_disks]=/usr/lib/nagios/plugins/check_disk -w 20% -c 10% -e

3. Finally, restart `nagios-nrpe-server`:

::

    $ sudo /etc/init.d/nagios-nrpe-server restart

4. Also, on `server01` restart `nagios`:

::

    $ sudo /etc/init.d/nagios3 restart



You should now be able to see the host and service checks in the Nagios CGI files. To access them point a browser to
`http://server01/nagios3`. You will then be prompted for the `nagiosadmin` username and password.
