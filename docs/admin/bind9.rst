.. _bind9:

Bind9 - Named Service
=====================

If your server will be DNS master or slave for your domains then this documentation will give basic info about **Bind9**
configuration.

In My example I'll use **lightningwolf.net** domain. Replace **lightningwolf.net** with your domain name.

For this example I'll use **192.168.0.1** IP address for reverse DNS. Replace it with your server IP address. In most of
situations configuration for reverse DNS is not required.


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

Configure the main Bind files. For Ubuntu instead of editing the file ``named.conf`` we will edit another files ::

    $ sudo vim /etc/bind/named.conf.local

This is where we will insert our zones. Insert this in the named.conf.local file:

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

If there is a need to setup forwarders there is another file to edit::

    $ sudo vim /etc/bind/named.conf.options

Replace **192.168.1.1** below with the address of your provider's DNS server

| forwarders {
|    # Replace the address below with the address of your provider's DNS server
|    123.123.123.123;
| };
