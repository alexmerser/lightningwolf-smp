.. _bind9:

Bind9 - Named Service
=====================

Best place to start is `Domain Name Service (DNS) <https://help.ubuntu.com/lts/serverguide/dns.html>`_

If your server will be DNS master or slave for your domains then this documentation will give basic info about **Bind9**
configuration.

* In My example I'll use **example.com** domain. Replace **example.com** with your domain name.
* For this example I'll use **192.168.0.1** IP address for reverse DNS. Replace it with your server IP address.
* For this example **ns1.example.com** IP address is  **192.168.0.1** and this is primary master DNS server.
* For this example **ns2.example.com** IP address is  **192.168.0.2** and this is secondary slave DNS server.

Installation
------------

Using console command ::

    $ sudo apt-get install bind9

A very useful package for testing and troubleshooting DNS issues is the dnsutils package. Very often these tools will be
installed already, but to check and/or install dnsutils enter the following ::

    $ sudo apt-get install dnsutils

Configuration
-------------

Configure the main Bind files. For Ubuntu instead of editing the file ``named.conf`` we will edit another files.

Caching Nameserver
^^^^^^^^^^^^^^^^^^

The default configuration is setup to act as a caching server. All that is required is simply adding the IP Addresses of
your ISP's DNS servers. Simply uncomment and edit the following in ``/etc/bind/named.conf.options``:

.. raw:: html

    <pre>
    forwarders {
                    1.2.3.4;
                    5.6.7.8;
               };
    </pre>

Replace **1.2.3.4** and **5.6.7.8** with the IP Adresses of actual nameservers.

Now restart the DNS server, to enable the new configuration. From a terminal prompt ::

    $ sudo service bind9 restart

See `dig <https://help.ubuntu.com/lts/serverguide/dns-troubleshooting.html#dns-testing-dig>`_ for information on testing
a caching DNS server.

Primary Master
^^^^^^^^^^^^^^

In this section BIND9 will be configured as the Primary Master for the domain **example.com**. Simply replace
**example.com** with your FQDN (Fully Qualified Domain Name).

Forward Zone File
"""""""""""""""""

Edit ``/etc/bind/named.conf.local`` ::

    $ sudo vim /etc/bind/named.conf.local

This is where we will insert our zones.


.. raw:: html

    <pre>
    # This is the zone definition.
    zone "example.com" {
            type master;
            file "/etc/bind/db.example.com";
    };
    </pre>

Now use an existing zone file as a template to create the /etc/bind/db.example.com file ::

    $ sudo cp /etc/bind/db.local /etc/bind/db.example.com

Edit the new zone file ``/etc/bind/db.example.com`` ::

    $ sudo vim /etc/bind/db.example.com

In my situation in the end I have this zone file:

.. raw:: html

    <pre>
    $TTL 86400 ; 1 day
    @       IN      SOA     ns1.example.com. root.ns1.example.com. (
                                    2013111101
                                    28800
                                    7200
                                    432000
                                    86400
    )
                    IN      NS      ns1.example.com.
                    IN      NS      ns2.example.com.
                    MX      10      mta.example.com.

    @               IN      A       192.168.0.3
    mta             IN      A       192.168.0.4
    www             IN      A       192.168.0.3
    ns1             IN      A       192.168.0.1
    ns2             IN      A       192.168.0.2
    sds             IN      CNAME   sds.tiktalik.com.
    *               IN      A       192.168.0.3
    </pre>

Where:

  * **mta** - mail server name
  * **ns1** - my first master dns server name
  * **ns2** - my secondary slave dns server name
  * **www** - standard form web server name
  * **sds** - example of ``CNAME`` in this situation is for bucket **sds.example.com** in Tiktalik like S3 file store
  * **\*** - all rest transfer to ``192.168.0.3`` in my example

Once you have made changes to the zone file BIND9 needs to be restarted for the changes to take effect ::

    $ sudo service bind9 restart

Reverse Zone File
"""""""""""""""""

Now that the zone is setup and resolving names to IP Adresses a Reverse zone is also required. A Reverse zone allows DNS
to resolve an address to a name.

Edit ``/etc/bind/named.conf.local`` and add the following:

.. raw:: html

    <pre>
    zone "0.168.192.in-addr.arpa" {
            type master;
            file "/etc/bind/db.192";
    };
    </pre>

Replace **0.168.192** with the first three octets of whatever network you are using. Also, name the zone file
``/etc/bind/db.192`` appropriately. It should match the first octet of your network.

Now create the /etc/bind/db.192 file ::

    $ sudo cp /etc/bind/db.127 /etc/bind/db.192

Next edit ``/etc/bind/db.192`` changing the basically the same options as ``/etc/bind/db.example.com``:

.. raw:: html

    <pre>
    ;
    ; BIND reverse data file for local 192.168.1.XXX net
    ;
    $TTL    604800
    @       IN      SOA     ns1.example.com. root.example.com. (
                                  2         ; Serial
                             604800         ; Refresh
                              86400         ; Retry
                            2419200         ; Expire
                             604800 )       ; Negative Cache TTL
    ;
    @       IN      NS      ns1.
    1       IN      PTR     ns1.example.com.
    2       IN      PTR     ns2.example.com.
    3       IN      PTR     example.com.
    4       IN      PTR     mta.example.com.
    </pre>

After creating the reverse zone file restart BIND9 ::

    $ sudo service bind9 restart

Secondary Master
^^^^^^^^^^^^^^^^

Once a Primary Master has been configured a Secondary Master is needed in order to maintain the availability of the
domain should the Primary become unavailable.

First, on the Primary Master server, the zone transfer needs to be allowed. Add the allow-transfer option to the example
Forward and Reverse zone definitions in ``/etc/bind/named.conf.local``:

.. raw:: html

    <pre>
    zone "example.com" {
            type master;
            file "/etc/bind/db.example.com";
            allow-transfer { 192.168.0.2; };
            also-notify { 192.168.0.2; };
    };

    zone "0.168.192.in-addr.arpa" {
            type master;
            file "/etc/bind/db.192";
            allow-transfer { 192.168.0.2; };
            also-notify { 192.168.0.2; };
    };
    </pre>

Replace **192.168.0.2** with the IP Address of your Secondary nameserver.

Restart BIND9 on the Primary Master ::

    $ sudo service bind9 restart

Next, on the Secondary Master, install the bind9 package the same way as on the Primary. Then edit the
``/etc/bind/named.conf.local`` and add the following declarations for the Forward and Reverse zones:


.. raw:: html

    <pre>
    zone "example.com" {
            type slave;
            file "db.example.com";
            masters { 192.168.0.1; };
    };

    zone "1.168.192.in-addr.arpa" {
            type slave;
            file "db.192";
            masters { 192.168.0.1; };
    };
    </pre>

Replace **192.168.0.1** with the IP Address of your Primary nameserver.

Restart BIND9 on the Secondary Master ::

    $ sudo service bind9 restart

check  ``/var/log/syslog``.

Troubleshooting
---------------

Best placec to check is `Troubleshooting <https://help.ubuntu.com/lts/serverguide/dns-troubleshooting.html>`_.

Checking if ns is visable. For example ::

    $ nslookup ns1.example.com ns1.domena.pl

Use your provider nameserver.