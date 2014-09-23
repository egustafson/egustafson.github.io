:title: Diskless Install of Ubuntu with PXE & Dnsmasq
:date: 2014-08-19
:slug: pxe-install-ubuntu
:author: Eric Gustafson
:tags: PXE, install, debian, ubuntu, preseed, dnsmasq, virtualbox
:status: draft

The other day I received a "server" (HP Z620) as part of work.  I set out to
integrate it into a new subnet to be used like a mini-cloud LAN.  Since my "lab"
is a floor down from my office my first goal was to make this "server" remote
everything, right down to the BIOS.  This way I could reboot and even *reload*
the bare metal OS remotely.  The Z620 has `Intel AMT`_ and I've progressed that
to the point where I can remotely power on/off the machine -- more on that in
another article.  The next step was to setup PXE_ booting.

In my past I've setup PXE environments, but as I started to reason through what
I needed I realized that I had over simplified.  Did I want to PXE install, or
PXE boot a kernel with the root filesystem on local disk?  Both actually, and
maybe some other `PXE acrobatics`_.  Step one: PXE boot into an installation and
then automate the installation with a preseed_ file.

.. _`Intel AMT`:
   https://en.wikipedia.org/wiki/Intel_Active_Management_Technology
.. _PXE: https://en.wikipedia.org/wiki/Preboot_Execution_Environment
.. _preseed: https://help.ubuntu.com/14.04/installation-guide/amd64/apb.html

PXE Boot to Install - Ubuntu
============================

The `Ubuntu Installation Guide`_ covers most of what is described below.  The
one exception is that I prefer Dnsmasq_ for its simplicity, and every PXE boot
example I found seems to want to explain the process with the amalgamation of
the ISC DHCP server, and one of the many, execellent tftpd servers.  Dnsmasq was
made for this, why is a more complex tool chain being consistently pushed?  -- I
don't know.

Additionally, I, like many people, like prototyping in a virtual environment.  I
use VirtualBox_, and VirtualBox supports PXE booting.  In fact, there are a
couple of ways to do a PXE boot in VirtualBox.  This example will **not** use
any of VirtualBox's built-in PXE boot features.  Instead, two (virtual) hosts
will be configured, one as the PXE boot server, and a second as the booted
client.  This pattern mimics physical hardware, and, in fact, should be
reproducable on physical equipment by simply ignoring the VirtualBox commentary.

.. _`Ubuntu Installation Guide`: https://help.ubuntu.com/14.04/installation-guide/amd64/index.html
.. _Dnsmasq: http://www.thekelleys.org.uk/dnsmasq/doc.html
.. _VirtualBox: https://www.virtualbox.org/

Prerequesites
-------------

1. (optional) VirtualBox, host OS doesn't matter.  This article is written with
   VirtualBox instructions, ignoring the VirtualBox parts and using physical
   hardware should just work.
2. A linux server.  Package install commands based on Ubuntu, any distribution
   should work; infact any OS with Dnsmasq should work the same.
3. A client host -- the disk on this machine will be **erased**.  The example
   will use a newly created VirtualBox host.
4. A "dhcp free" LAN.  In this example, a VirtualBox "Internal Network" will
   serve as the LAN.

PXE, DHCP, and a "clean" LAN
----------------------------

For those familiar with DHCP's broadcast use of the LAN, this section may be
safely skipped.

The first step in a "PXE Boot" is for the client host to perform a DHCP_
request, or more precisely a DHCP discovery.  This amounts to the client sending
a broadcast IP message on the connected LAN.  Because the client knows nothing
of itself at this point, it can only broadcast a message requesting it's
configuration, the "C" in DHCP.  Many LAN's support DHCP, including the default
VirtualBox "NAT" LAN.  In order to PXE boot a specific response to the DHCP
request must be given; the culmunation of this article in fact.  If the PXE
booting client is "placed" on a LAN that already has a DHCP service present then
it is possible that the existing service will respond, and respond with a
generic response, not the PXE specific response this article details crafting.

For this reason, the "dhcp free" LAN is stated above as a prerequisite.  If you
know you have a DHCP free physical LAN then you're good; many home "routers"
provide DHCP as part of their functionality -- you've been warned.

VirtualBox's default network is the "NAT" network and it has a DHCP service
embedded in the VirtualBox 'controller'.  This LAN network can not be used.
Details for configuring multiple VirtualBox networks will be given below for
this very reason.

.. _DHCP: https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol

Configuring the VirtualBox Hosts and Network(s)
-----------------------------------------------



Configuring Dnsmasq on the PXE Server
-------------------------------------


Booting the PXE Client
----------------------



Preseeding to Automate the Install
==================================

TBD - coming in the |2nd| part of this article.

.. |2nd| replace:: 2\ :sup:`nd`


To be continued? ...
====================

Ideas for follow on articles around this topic:

- PXE Boot a "cloud" image, (think Amazon AMI/LXC ubuntu-cloud like), on bare
  metal -- there are some gotcha's in this.
- PXE Boot every time.  A "production" environment where the bootloader is PXE,
  the kernel comes across the network, and the filesystem already exists on one
  of {local disk, SAN_, NAS_}.
- _`PXE Acrobatics`: An advanced, intellegent system for PXE booting where
  sometimes an existing system is booted, and sometimes the host is
  reprovisioned, i.e. re-installed.


.. _SAN: https://en.wikipedia.org/wiki/Storage_area_network
.. _NAS: https://en.wikipedia.org/wiki/Network-attached_storage

.. Local Variables:
.. fill-column: 80
.. End:
