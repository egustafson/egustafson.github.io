:title: Quintessential Ceph
:date: 2016-04-20
:slug: quintessential-ceph
:author: Eric Gustafson
:tags: Linux, ceph, storage, persistence, install, ubuntu

The following is my distillation of how to install Ceph_ in the most minimal
way.  This method of installation is *NOT* the {right, correct, best, ...} way
to install Ceph.  It is what I could discern as the most minimal way to install
the smallest set of Ceph components to have a minimally running system.   I did
this to better understand Ceph and hope it will help others as well.

.. _Ceph: http://docs.ceph.com

Architecture & what's needed
============================

The `Ceph Architecture`_ page starts with both a good diagram and description of
what makes up the cluster.


.. _Ceph Architecture: http://docs.ceph.com/docs/master/architecture/


Minimal Steps to create a Ceph cluster
======================================

The architecture:  4 Hosts

* 3x Storage Nodes  (have second "storage" drive)
  * hostnames:  ceph-osd{0,1,2}
* 1x Monitor Node
  * hostname:  ceph-mon0
    

Prerequisites
-------------

:Hosts:   4 -- ok, this isn't the minimum, but for this example it is.
:OS:      Ubuntu (4G root is sufficient) // I used Wily (15.10) Server
:OSD Disk:  A second "disk" for the OSD hosts.  (sdb)
:DNS:     DNS should work to resolve the host names.  (or /etc/hosts)

The above can be accomplished in visualized environments.  Make sure your VM
environment has networking such that all of the hosts can connect to each other
on the same subnet.

Install Ceph Software
---------------------

.. code-block:: tcsh

   > sudo apt-get install ceph

Will install the Ceph components needed.  Perform this on all hosts.

ceph.conf Configuration file
----------------------------

The following configuration file will be used on all hosts; it lives in
`/etc/ceph/ceph.conf`:

.. code-block:: tcsh
                
   fsid = d4b1b3b2-3bbb-4487-93ef-068d3ee73a22

   mon_initial_members = a
   mon_host = 10.3.7.91

   auth_cluster_required = none
   auth_service_required = none
   auth_client_required = none

Two entries in this file should be changed:

* fsid = `<uuid>`    ## use 'uuidgen' to generate a unique UUID

* mon_host = <ip-addr>  ## place the actual IP of 'ceph-mon0' here.

Configure the Monitor host
--------------------------

* Monitor host:  ceph-mon0

1. Place the `ceph.conf` file from the previous step in /etc/ceph.  Owned by
   root and world readable (0644).

2. Run `ceph-mon` to initialize the "mon data" directory (/var/lib/ceph/mon).
   This monitor, the only monitor in this example, will be monitor 'a'.  The `-i
   a` flag identifies the monitor as having id 'a'.  After running this command
   there will be a `/var/lib/ceph/mon/ceph-a` directory.  The 'ceph' corresponds
   to the cluster name and the '-a' corresponds to monitor id 'a'.

.. code-block:: tcsh
   
   > sudo ceph-mon --cluster=ceph -i a -f --mkfs

3. Start `ceph-mon` as a daemon, (now that the data directory is initialized.

.. code-block:: tcsh
   
   > sudo ceph-mon --cluster=ceph -i a

4. Verify the monitor is running (from ceph-mon0)

.. code-block:: tcsh
   
   > ceph health
   HEALTH_ERR 64 pgs stuck inactive; 64 pgs stuck unclean; no osds

It is expected that the health is in error; there are no osd daemons running
yet.  If the call does not return, (hangs), that is the indicator of a problem.

Configure and join each OSD host
--------------------------------

(optional:  Running `ceph -w` on host ceph-mon0 will allow you to "tail" the
activities of the cluster.  You should see output after running each `ceph-disk`
command.  The `ceph -w` command can actually be run from any host configured to
interact with the ceph cluster, but ceph-mon0 is convenient in this case.)

Repeat this process for each OSD host:  `mon-osd{0,1,2}`

1. Copy and install the `ceph.conf` file in /etc/ceph.  Owned by root and world
   readable (0644).   [do not change the mon_host IP address.]

2. Ensure /dev/sdb is *UNMOUNTED* and available for both partitioning and
   formatting.  *All data on /dev/sdb will be DESTROYED*

.. code-block:: tcsh
   
   > sudo ceph-disk prepare \
       --cluster ceph \
       --cluster-uuid d4b1b3b2-3bbb-4487-93ef-068d3ee73a22 \
       --fs-type btrfs \
       /dev/sdb
   Creating new GPT entries.
   Setting name!
   partNum is 1
   REALLY setting name!
   The operation has completed successfully.
   Setting name!
   partNum is 0
   REALLY setting name!
   The operation has completed successfully.
   WARNING: --leafsize is deprecated, use --nodesize
   btrfs-progs v4.0
   See http://btrfs.wiki.kernel.org for more information.
   
   Turning ON incompat feature 'extref': increased hardlink limit per file to 65536
   Turning ON incompat feature 'skinny-metadata': reduced-size metadata extent refs
   fs created label (null) on /dev/sdb1
        nodesize 32768 leafsize 32768 sectorsize 4096 size 15.00GiB
   Warning: The kernel is still using the old partition table.
   The new table will be used at the next reboot or after you
   run partprobe(8) or kpartx(8)
   The operation has completed successfully.
        
   > ceph df
   GLOBAL:
       SIZE       AVAIL      RAW USED     %RAW USED
       15358M     15089M       33440k          0.21
   POOLS:
       NAME     ID     USED     %USED     MAX AVAIL     OBJECTS
       rbd      0         0         0         5029M           0

   > ps -ef | grep ceph-osd
   root    2248   1  0 19:08 ?   00:00:00 /usr/bin/ceph-osd --id 0 --foreground --cluster ceph -c /etc/ceph/ceph.conf
                   
In the above example the initial size of /dev/sdb was 20G and preparing the disk
left approximately 155358M usable for storage.  The remainder went to the
partition used for the Ceph journal.

After applying the above command to the 2nd and 3rd (ceph-mon{1,2}) hosts you
will see an appropriate increase in the available storage.

Observing the output of `ps` you see that the `ceph-disk prepare` command has
started the OSD daemon as well.  Upon reboot `ceph-osd` will be automatically
started as a service.

*Note:* `ceph-mon` is not configured to autostart using _this_ set of
instructions.

Repeat for hosts mon-osd{1,2}

Done.


Exercise the Ceph cluster
=========================

The following commands will demonstrate basic cluster functionality; they can be
performed from any host that has:

1. Direct network connectivity to the cluster (no NAT - in case you used
   Virtualbox, et. al.)
2. The `ceph.conf` file from above placed in /etc/ceph and readable.
3. The `ceph` Ubuntu package installed (from step 1).

A convenient, but not necessary, host to use are any of the hosts you just
installed.

List and create a pool for storage
----------------------------------

Note:  the following commands do not require the use of `sudo`.  Authentication
would be acomplished via the cephx protocol if it had not been disabled in the
ceph.conf file, (the last three lines set the "auth" parameters to 'none').

.. code-block:: tcsh

   > ceph osd pool ls
   rbd

Ceph creates a default pool named 'rbd' when initialized.

.. code-block:: tcsh

   > rados mkpool data
   successfully created pool data

   > rados df
   pool name        KB  objects  clones  degraded  unfound   rd   rd KB   wr   wr KB
   data              0        0       0         0        0    0       0    0       0
   rbd               0        0       0         0        0    0       0    0       0
   total used    102176       0
   total avail 46354496
   total space 47182788
   
Place a file directly in the 'data' pool
----------------------------------------

.. code-block:: tcsh

   > touch test-file.out
   > rados put -p data test-file.out test-file.out
   > rados ls -p data
   test-file.out

This concludes the quintessential Ceph installation and simple demonstration that the cluster is functioning.

Thank you - Eric
  
.. Local Variables:
.. fill-column: 80
.. End:

..  LocalWords:  Ceph ceph Gustafson
