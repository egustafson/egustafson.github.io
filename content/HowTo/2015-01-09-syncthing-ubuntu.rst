:title: Syncthing on Ubuntu
:date: 2015-01-09
:slug: syncthing-ubuntu
:author: Eric Gustafson
:tags: install, ubuntu, sync, syncthing

Last month, after looking at `BitTorrent Sync`_ and realizing it was
encrypted and private, but *not* open source, I went digging for an
alternative.  I found the perfect project, for me:  Syncthing_.  The
project is still relatively young and while it has proven to be
perfectly functional, it did not come with batteries included -- an
installer package.   It does come with init scripts for some
environments, but not for Ubuntu -- at least until Ubuntu transitions
to systemd.  So, without further ado, here's what I did to install
Syncthing as daemon (service) under Ubuntu.

.. _`BitTorrent Sync`:  http://www.getsync.com/
.. _`Syncthing`: http://syncthing.net/

:Run as:         User: 'synct' // Group: 'synct'
:Service Name:   syncthing
:Install to:     /opt/syncthing
:Config:         /opt/syncthing/etc
:GUI:            Exposed at 0.0.0.0:8080
:Public Access:  Firewall port redirect.

----
                 
There's nothing out of the ordinary about installing Syncthing as a service.
Above are the details I chose for how I'd install the service.  There are two
points are worth noting.  First, after the initial install the service's
configuration is editable through the web-gui; the XML config will be in
/opt/syncthing/etc.  Second, sync-able repositories do not have to live in the
installation directory.  Installing is mostly about creating the extra fluff
needed to have init start the binary.

A reminder - this is aimed at an **Ubuntu** system.  Specifically, 14.10
(Utopic) was used, although earlier versions should work too.  When Ubuntu
transitions to systemd as an init system, the included Upstart script will not
be applicable.  (Current rumor is that the transition will be in the next
release -- caveat emptor)

1. Create User and Group for the Daemon
---------------------------------------

.. code-block:: tcsh

   ## add home dir first so adduser does not populate it with skel files.
   sudo mkdir /opt/syncthing
   sudo mkdir /opt/syncthing/etc
   sudo adduser --system --group --home /opt/syncthing synct
   sudo chown -R synct.synct /opt/syncthing

The ``synct`` group provides the opportunity to add authorized users to make
'syncable' folders with the ``synct`` group.  Those users can manage their
folder(s) with out the need for sudo/root privilege.

2. Install the Syncthing Binary
-------------------------------

Fetch the binary from the `Syncthing GitHub Project`_.  The releases URL is:
https://github.com/syncthing/syncthing/releases.  Download the tarball
appropriate for your architecture.  (The example uses ``amd64``, and version
0.10.18) 

.. _`Syncthing GitHub Project`: https://github.com/syncthing/syncthing

.. code-block:: bash

   cd /tmp
   tar -xvf /path-to/syncthing-linux-amd64-v0.10.18.tar.gz
   sudo mkdir /opt/syncthing/bin
   sudo cp syncthing-linux-amd64-v0.10.18/syncthing /opt/syncthing/bin

The only file needed from the release tarball is the executable itself.  The
executable is tar'ed with execute permission, but it never hurts to verify its
executable. 

4. Install an Upstart "Script"
------------------------------

Install the following Upstart configuration file in ``/etc/init/syncthing.conf``

.. code-block:: text

   description  "syncthing daemon"
   author       "Eric Gustafson <egustafson in launchpad>"

   start on (local-filesystems and net-device-up IFACE!=lo)
   stop on runlevel [!2345]

   setuid synct
   setgid synct

   env HOME=/opt/syncthing

   exec /opt/syncthing/bin/syncthing -home /opt/syncthing/etc
   
A couple of notes on the conf file:

1. Setting the ``HOME`` env lets syncthing know where to create the default,
   ``Sync`` folder on initial start-up.  I had problems before I added this
   stanza.

2. Using the "``-home /opt/syncthing/etc``" flag instructs syncthing to place
   all configuration files *directly* into the ``etc`` directory.  If this flag
   is missing it will place the configuration in a hidden directory under
   ``$HOME``.

It would be nice to get a list of supported environment variables and command
line switches, but the docs are not there yet.  Conversely, I could "read the
source luke", so I should stop whining and go contribute ;)

   
5. Start and Verify the Service
-------------------------------

If the stars are aligned, then the service will start:

.. code-block:: bash

   sudo service syncthing start
   sudo tail -f /var/log/upstart/syncthing.log

At this point the service is (hopefully) up.  There is a small problem, however:
the configuration created on first-run restricts the web-gui to loopback only
(127.0.0.1).  This is fine if the machine is your desktop, but can be a snag if
its remote.  The config file can be edited by hand to change this.

In preparation for changing the listening address for the web-gui:

.. code-block:: bash

   sudo service syncthing stop


6. Modify the Configuration to expose the Web GUI
-------------------------------------------------

Edit the config file:  ``/opt/syncthing/etc/config.xml``

.. code-block:: bash

   ## syncthing changes the permissions on etc, sudo is required
   sudo emacs /opt/syncthing/etc/config.xml

The following line should be changed as depicted.  The important aspect is to
change the ``127.0.0.1`` to the wildcard address, ``0.0.0.0``.  [The port could
be changed too, if need be.]

.. code-block:: xml

   <gui enabled="true" tls="false">
       <address>0.0.0.0:8080</address>
       ...
   </gui>

Now restart the service

.. code-block:: bash

   sudo service syncthing start

and point a web browser at port 8080 of the host.

7. (Optional) Firewall Port Redirect
------------------------------------

At this point you have a perfectly good, working Syncthing -- congratulations.

However, if your host is behind a firewall it may not be reachable for
sync-ing.  The first point:  if you have a consumer firewall that supports UPnP
then Syncthing is likely visible as it supports, and enables by default, UPnP.
If you don't have UPnP enabled on your firewall or the Syncthing instance is not
visible then following the "`Firewalls and Port Forwards`_" instructions on the
`wiki`_ will help you resolve the issue.

.. _`Firewalls and Port Forwards`:
       https://github.com/syncthing/syncthing/wiki/Firewalls-and-Port-Forwards
.. _`wiki`: https://github.com/syncthing/syncthing/wiki

In short: plumb TCP port 22000 through from your firewall to the server.  Port
22000 is the default port for the Block Exchange Protocol [1]_ (BEP), and the
only port necessary for a remote agent to connect with your server.

.. [1] The protocols Syncthing uses are documented here:  https://github.com/syncthing/specs


----

That's it, you're done.  Happy syncing.

.. Local Variables:
.. fill-column: 80
.. End:
