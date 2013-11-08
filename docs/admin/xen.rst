.. _xen:

XEN DomU
========

Good place to start is `Ubuntu help for XEN <https://help.ubuntu.com/community/Xen#Creating_vms>`_. Rest of this
documentation is based on it.

Creation of our work server instance
------------------------------------

**All steps as root**

1. First step you should check what distributions ara avaiable ::

    $ cd /usr/lib/xen-tools/
    $ ls -la

   If there is not `raring.d` then ::

    $ ln -s karmic.d raring.d


2. Second step is to create instance ::

    $ xen-create-image --lvm <lvm name>  --dist <distribution>  --hostname=<instance hostname> --dhcp

   For this example, assume:
     * **<lvm name>** = myLvmVolume
     * **<instance hostname>** = wolf
     * **<distribution>** = raring

   When all is OK there will be information and root password in it.

3. Third step is to first boot created instance ::

    $ xm create /etc/xen/wolf.cfg -c


   If there is a need to recreate then ::

    $ lvremove /dev/myLvmVolume/wolf-*
    $ rm /etc/xen/wolf.cfg

   and return to **Step 2**

4. Fourth is to configure created instance and adapt it to our needs

  * Change root disk size ::

    $ lvresize -L +10g /dev/myLvmVolume/wolf-disk
    $ e2fsck -f /dev/myLvmVolume/wolf-disk
    $ resize2fs /dev/myLvmVolume/wolf-disk
    $ e2fsck -f /dev/myLvmVolume/wolf-disk


  * Create ``var`` volume - in my example 60GB ::

    $ lvcreate -n wolf-var -L 60g myLvmVolume
    $ mkfs.ext3 /dev/myLvmVolume/wolf-var

  * Change XenDomU configuration file ::

    $ vi /etc/xen/wolf.cfg

    and made changes:

    | root = '/dev/xvda2 ro'
    | disk = [
    |   'phy:/dev/myLvmVolume/wolf-disk,xvda2,w',
    |   'phy:/dev/myLvmVolume/wolf-swap,xvda1,w',
    |   'phy:/dev/myLvmVolume/wolf-var,xvda3,w',
    | ]


  * Transfer existing ``var`` folder data to new one ::

    $ mkdir /mnt/wolf
    $ mount /dev/myLvmVolume/wolf-disk /mnt/wolf/
    $ mv /mnt/wolf/var /mnt/wolf/var-copy
    $ mkdir /mnt/wolf/var
    $ mount /dev/myLvmVolume/wolf-var /mnt/wolf/var
    $ mv /mnt/wolf/var-copy/* /mnt/wolf/var/
    $ rmdir /mnt/wolf/var-copy/

  * New settings in instance fstab file ::

    $ vi /mnt/wolf/etc/fstab

    and made changes:

    | /dev/xvda3 /var ext3 noatime,nodiratime,errors=remount-ro 0 1


  * Umount ::

    $ umount /mnt/wolf/var
    $ umount /mnt/wolf


  * Start final version of our server instance ::

    $ xm create /etc/xen/wolf.cfg -c
