.. _bind9:

Bind9 - Named Service
=====================

If your server will be DNS master or slave for your domains then this documentation will give basic info about **Bind9**
configuration.

In My example I'll use **lightningwolf.net** domain. Replace **lightningwolf.net** with your domain name.

For this example I'll use **192.168.0.1** IP address for reverse DNS. Replace it with your server IP address. In most of
situations configuration for reverse DNS is not required.

For this example ns1.lightningwolf.net IP address is  **192.168.0.1** and this is master DNS server.
For this example ns2.lightningwolf.net IP address is  **192.168.0.2** and this is slave DNS server.

Installation
------------

Using console command ::

    $ sudo apt-get install bind9 bind9-doc

Pre configuration
-----------------

My bind conf folder structure:

  * **/etc/bind** - Main configuration folder
  * **/etc/bind/pri** - Primary domain zone folder (for zone type: **master**)
  * **/etc/bind/sec** - Secondary domain zone folder (for zone type: **slave**)

Folders ``/etc/bind/pri`` and ``/etc/bind/sec`` must be created ::

    $ sudo mkdir /etc/bind/pri
    $ sudo mkdir /etc/bind/sec

Because ``/etc/bind/sec`` folder must have write access ::

    $ sudo chown bind /etc/bind/sec

Configuration
-------------

Configure the main Bind files. For Ubuntu instead of editing the file ``named.conf`` we will edit another files.

named.conf.local
^^^^^^^^^^^^^^^^

Edit it by vim ::

    $ sudo vim /etc/bind/named.conf.local

This is where we will insert our zones.

Insert this in the named.conf.local file for **master** dns server:

.. raw:: html

    <pre>
    # This is the zone definition.
    zone "lightningwolf.net" {
        type master;
        file "/etc/bind/pri/lightningwolf.net.db";
    };
    </pre>

Insert this in the named.conf.local file for **slave** dns server:

.. raw:: html

    <pre>
    # This is the zone definition.
    zone "lightningwolf.net" IN {
       type slave;
       file "sec/lightningwolf.net.db";
       masters { 192.168.0.1; };
    };
    </pre>

**If we need reverse DNS also add into master dns server:**

.. raw:: html

    <pre>
    # This is the zone definition for reverse DNS.
    zone "0.168.192.in-addr.arpa" {
        type master;
        file "/etc/bind/pri/rev.0.168.192.in-addr.arpa";
    };
    </pre>

named.conf.options
^^^^^^^^^^^^^^^^^^
Edit it by vim ::

    $ sudo vim /etc/bind/named.conf.options

Because I have slave DNS there is a need to add it`s IP to ``allow-transfer`` for **master**:

.. raw:: html

    <pre>
    // My network
    allow-transfer {
            192.168.1.2;
    };
    </pre>

Because I have slave DNS there is a need to add it`s IP to ``allow-transfer`` for **slave**:

.. raw:: html

    <pre>
    // My network
    allow-transfer {
            192.168.1.1;
    };
    </pre>

**If there is a need to setup forwarders**

Replace **192.168.1.1** below with the address of your provider's DNS server

.. raw:: html

    <pre>
    forwarders {
       192.168.1.1;
    };
    </pre>


zone.db
^^^^^^^

Now we need to edit master zone file ::

    $ sudo vim /etc/bind/pri/lightningwolf.net.db

.. raw:: html

    <pre>
    @       IN      SOA     ns1.lightningwolf.net. root.ns1.lightningwolf.net. (
                                    2013111101
                                    28800
                                    7200
                                    432000
                                    86400
    )
                    IN      NS      ns1.lightningwolf.net.
                    IN      NS      ns2.lightningwolf.net.
                    MX      10      mta.lightningwolf.net.

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
  * **sds** - example of ``CNAME`` in this situation is for bucket sds.lightningwolf.net in Tiktalik like S3 file store
  * **\*** - all rest transfer to ``192.168.0.3`` in my example

Optional rev.zone.db
^^^^^^^^^^^^^^^^^^^^

Let's create the reverse DNS zone file ::

    sudo vim /etc/bind/pri/rev.0.168.192.in-addr.arpa

Copy and paste the following text, modify as needed:

.. raw:: html

    <pre>
    // The number before IN PTR lightningwolf.net is the machine address of the DNS server. in my case, it's 3, as my IP address is 192.168.0.3.
    @ IN SOA ns1.lightningwolf.net. root.ns1.lightningwolf.net. (
                                    2006081401;
                                    28800;
                                    604800;
                                    604800;
                                    86400
    )

                    IN    NS     ns1.lightningwolf.net.
                    IN    NS     ns2.lightningwolf.net.
    3               IN    PTR    lightningwolf.net
    </pre>

Run and Checks
--------------

Ok, now you just need to restart bind ::

    $ sudo service bind9 restart

We can now test the new DNS server...

Modify the file resolv.conf ::

    $ sudo vim /etc/resolv.conf

Enter the following:

.. raw:: html

    <pre>
    search lightningwolf.net
    nameserver 192.168.0.1
    </pre>

Now, test your DNS ::

    $ dig lightningwolf.net
