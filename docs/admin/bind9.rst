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

| # This is the zone definition.
| zone "lightningwolf.net" {
|     type master;
|     file "/etc/bind/pri/lightningwolf.net.db";
| };

   If we need reverse DNS also add:

| # This is the zone definition for reverse DNS.
| zone "1.0.168.192.in-addr.arpa" {
|     type master;
|     file "/etc/bind/rev/rev.1.0.168.192.in-addr.arpa";
| };

Insert this in the named.conf.local file for **slave** dns server:

| # This is the zone definition.
| zone "lightningwolf.net" IN {
|    type slave;
|    file "sec/lightningwolf.net.db";
|    masters { 192.168.0.1; };
| };

named.conf.options
^^^^^^^^^^^^^^^^^^
Edit it by vim ::

    $ sudo vim /etc/bind/named.conf.options

Because I have slave DNS there is a need to add it`s IP to ``allow-transfer`` for **master**:

| // My network
| allow-transfer {
|         192.168.1.2;
| };

Because I have slave DNS there is a need to add it`s IP to ``allow-transfer`` for **slave**:

| // My network
| allow-transfer {
|         192.168.1.1;
| };

**If there is a need to setup forwarders**

Replace **192.168.1.1** below with the address of your provider's DNS server

| forwarders {
|    192.168.1.1;
| };
